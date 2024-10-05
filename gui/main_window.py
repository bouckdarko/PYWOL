# gui/main_window.py

import sys
import os
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
)
from PySide6.QtCore import Qt, QSize, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer

from gui.theme_manager import ThemeManager
from gui.widgets.menu_bar import MenuBar
from gui.widgets.device_list import DeviceList
from gui.settings_window import SettingsWindow
from gui.add_device_window import AddDeviceWindow
from gui.wake_device_window import WakeDeviceWindow

# Fonction resource_path pour gérer les ressources avec PyInstaller
def resource_path(relative_path):
    """Obtenir le chemin absolu de la ressource, fonctionne pour dev et pour PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Fonction pour charger et colorer les icônes SVG
def load_colored_icon(svg_path, color):
    # Charger le contenu du fichier SVG
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # Remplacer "currentColor" par la couleur désirée
    svg_content = svg_content.replace('currentColor', color)

    # Créer un QSvgRenderer à partir du contenu modifié
    svg_bytes = QByteArray(svg_content.encode('utf-8'))
    svg_renderer = QSvgRenderer(svg_bytes)

    # Créer un QPixmap pour rendre l'icône
    pixmap_size = QSize(24, 24)  # Taille de l'icône
    pixmap = QPixmap(pixmap_size)
    pixmap.fill(Qt.transparent)  # Rendre le fond transparent

    # Utiliser QPainter pour dessiner le SVG dans le QPixmap
    painter = QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()

    # Créer un QIcon à partir du QPixmap
    icon = QIcon(pixmap)
    return icon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyWoL")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        # Obtenir la taille de l'écran
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculer 50% de la taille de l'écran
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)

        # Redimensionner la fenêtre
        self.resize(window_width, window_height)

        # Centrer la fenêtre sur l'écran
        self.move(
            (screen_width - window_width) // 2,
            (screen_height - window_height) // 2
        )

        # Gestion du thème
        self.theme_manager = ThemeManager(self)
        self.setStyleSheet(self.theme_manager.get_stylesheet())

        # Obtenir la couleur d'accentuation
        accent_color = self.theme_manager.get_accent_color()

        # Création des icônes avec la couleur d'accentuation
        close_icon = load_colored_icon(resource_path("assets/interface/close_icon.svg"), accent_color)
        minimize_icon = load_colored_icon(resource_path("assets/interface/minimize_icon.svg"), accent_color)
        maximize_icon = load_colored_icon(resource_path("assets/interface/maximize_icon.svg"), accent_color)

        # Conteneur principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Barre de titre personnalisée
        self.title_bar = QWidget()
        self.title_bar.setObjectName("title_bar")
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setLayout(self.title_bar_layout)

        self.title_label = QLabel("PyWoL")
        self.title_label.setObjectName("title_label")
        self.title_bar_layout.addWidget(self.title_label)

        # Espacement flexible pour pousser les boutons à droite
        self.title_bar_layout.addStretch()

        # Boutons de la barre de titre avec icônes
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(minimize_icon)
        self.minimize_button.setIconSize(QSize(24, 24))
        self.minimize_button.setObjectName("minimize_button")

        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(maximize_icon)
        self.maximize_button.setIconSize(QSize(24, 24))
        self.maximize_button.setObjectName("maximize_button")

        self.close_button = QPushButton()
        self.close_button.setIcon(close_icon)
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setObjectName("close_button")

        self.title_bar_layout.addWidget(self.minimize_button)
        self.title_bar_layout.addWidget(self.maximize_button)
        self.title_bar_layout.addWidget(self.close_button)

        # Signaux des boutons de la barre de titre
        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.close)

        # Gestion du déplacement de la fenêtre
        self.offset = None

        # Ajout de la barre de titre au layout principal
        main_layout.addWidget(self.title_bar)

        # Layout principal horizontal
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Barre de menu à gauche
        self.menu_bar = MenuBar(self)
        content_layout.addWidget(self.menu_bar)

        # Contenu principal (liste des périphériques)
        self.device_list = DeviceList(self)
        content_layout.addWidget(self.device_list)

        # Signaux
        self.menu_bar.settings_triggered.connect(self.open_settings)
        self.menu_bar.add_device_triggered.connect(self.add_device)
        self.menu_bar.wake_mac_triggered.connect(self.wake_device_by_mac)

        # Variables pour le déplacement et le redimensionnement de la fenêtre
        self._is_resizing = False
        self._resize_direction = None
        self._margin = 5  # Marge pour détecter le redimensionnement

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start_pos = event.globalPos()
            self._is_resizing = self._resize_direction is not None
            if not self._is_resizing:
                if self.title_bar.rect().contains(event.pos()):
                    self._moving = True
                    self._move_offset = event.globalPos() - self.frameGeometry().topLeft()
                else:
                    self._moving = False

    def mouseMoveEvent(self, event):
        if self._is_resizing:
            self._resizeWindow(self._resize_direction, event.globalPos() - self._start_pos)
            self._start_pos = event.globalPos()
        elif getattr(self, '_moving', False):
            self.move(event.globalPos() - self._move_offset)
        else:
            self._updateCursorShape(event.pos())

    def mouseReleaseEvent(self, event):
        self._is_resizing = False
        self._moving = False
        self.setCursor(Qt.ArrowCursor)

    def _updateCursorShape(self, pos):
        rect = self.rect()
        left = abs(pos.x() - rect.left()) <= self._margin
        right = abs(pos.x() - rect.right()) <= self._margin
        top = abs(pos.y() - rect.top()) <= self._margin
        bottom = abs(pos.y() - rect.bottom()) <= self._margin

        if top and left:
            self.setCursor(Qt.SizeFDiagCursor)
            self._resize_direction = 'top_left'
        elif top and right:
            self.setCursor(Qt.SizeBDiagCursor)
            self._resize_direction = 'top_right'
        elif bottom and left:
            self.setCursor(Qt.SizeBDiagCursor)
            self._resize_direction = 'bottom_left'
        elif bottom and right:
            self.setCursor(Qt.SizeFDiagCursor)
            self._resize_direction = 'bottom_right'
        elif left:
            self.setCursor(Qt.SizeHorCursor)
            self._resize_direction = 'left'
        elif right:
            self.setCursor(Qt.SizeHorCursor)
            self._resize_direction = 'right'
        elif top:
            self.setCursor(Qt.SizeVerCursor)
            self._resize_direction = 'top'
        elif bottom:
            self.setCursor(Qt.SizeVerCursor)
            self._resize_direction = 'bottom'
        else:
            self.setCursor(Qt.ArrowCursor)
            self._resize_direction = None

    def _resizeWindow(self, direction, delta):
        rect = self.geometry()
        if direction == 'left':
            rect.setLeft(rect.left() + delta.x())
        elif direction == 'right':
            rect.setRight(rect.right() + delta.x())
        elif direction == 'top':
            rect.setTop(rect.top() + delta.y())
        elif direction == 'bottom':
            rect.setBottom(rect.bottom() + delta.y())
        elif direction == 'top_left':
            rect.setTopLeft(rect.topLeft() + delta)
        elif direction == 'top_right':
            rect.setTopRight(rect.topRight() + delta)
        elif direction == 'bottom_left':
            rect.setBottomLeft(rect.bottomLeft() + delta)
        elif direction == 'bottom_right':
            rect.setBottomRight(rect.bottomRight() + delta)

        self.setGeometry(rect)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def open_settings(self):
        settings_window = SettingsWindow(self)
        if settings_window.exec():
            # Mettre à jour le thème après modification des paramètres
            self.setStyleSheet(self.theme_manager.get_stylesheet())
            # Mettre à jour les icônes
            self.update_icons()

    def update_icons(self):
        # Méthode pour mettre à jour les icônes lorsque la couleur d'accentuation change
        accent_color = self.theme_manager.get_accent_color()
        close_icon = load_colored_icon(resource_path("assets/interface/close_icon.svg"), accent_color)
        minimize_icon = load_colored_icon(resource_path("assets/interface/minimize_icon.svg"), accent_color)
        maximize_icon = load_colored_icon(resource_path("assets/interface/maximize_icon.svg"), accent_color)

        self.close_button.setIcon(close_icon)
        self.minimize_button.setIcon(minimize_icon)
        self.maximize_button.setIcon(maximize_icon)

    def add_device(self):
        add_device_window = AddDeviceWindow(self)
        if add_device_window.exec():
            self.device_list.load_devices()

    def wake_device_by_mac(self):
        wake_window = WakeDeviceWindow(self)
        wake_window.exec()

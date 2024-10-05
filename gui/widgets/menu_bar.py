# gui/widgets/menu_bar.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QSize

class MenuBar(QWidget):
    settings_triggered = Signal()
    add_device_triggered = Signal()
    wake_mac_triggered = Signal()
    exit_triggered = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        # Ajout d'un label de titre
        title_label = QLabel("Menu")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title_label)

        # Séparateur
        self.layout.addSpacing(10)

        # Définition des boutons et de leurs signaux
        self.buttons_info = [
            ("Ajouter un périphérique", "add_icon.png", self.add_device_triggered.emit),
            ("Réveiller par MAC", "wake_icon.png", self.wake_mac_triggered.emit),
            ("Paramètres", "settings_icon.png", self.settings_triggered.emit),
            ("Quitter", "exit_icon.png", parent.close),
        ]

        # Création et ajout des boutons au layout
        self.buttons = []
        for label, icon_path, slot in self.buttons_info:
            button = QPushButton(label)
            button.setIcon(QIcon(icon_path))  # Placeholder pour l'icône
            button.setIconSize(QSize(24, 24))
            button.setStyleSheet("text-align: center; padding: 5px;")
            self.layout.addWidget(button)
            button.clicked.connect(slot)
            self.buttons.append(button)

        # Espacement flexible en bas pour pousser les boutons vers le haut
        self.layout.addStretch()

    def set_button_order(self, new_order):
        # Réorganiser les boutons selon le nouvel ordre
        # Supprimer tous les widgets du layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        # Ajouter le titre et le séparateur
        title_label = QLabel("Menu")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title_label)
        self.layout.addSpacing(10)

        # Ajouter les boutons dans le nouvel ordre
        for index in new_order:
            button = self.buttons[index]
            self.layout.addWidget(button)

        # Ajouter l'espacement flexible
        self.layout.addStretch()

# gui/settings_window.py

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QMessageBox,
    QColorDialog,
)
from PySide6.QtGui import QColor
from gui.theme_manager import ThemeManager
from database.settings_manager import SettingsManager
import bcrypt

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Paramètres")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.theme_manager = ThemeManager()
        self.settings_manager = SettingsManager()

        # Sélection du thème
        self.theme_label = QLabel("Thème :")
        self.layout.addWidget(self.theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Clair", "Sombre"])
        self.layout.addWidget(self.theme_combo)

        current_theme = self.theme_manager.get_theme()
        self.theme_combo.setCurrentText("Clair" if current_theme == 'light' else "Sombre")

        # Sélection de la couleur d'accentuation
        self.accent_color_label = QLabel("Couleur d'accentuation :")
        self.layout.addWidget(self.accent_color_label)

        self.accent_color_button = QPushButton()
        self.accent_color_button.setFixedHeight(30)
        self.layout.addWidget(self.accent_color_button)
        self.accent_color_button.clicked.connect(self.choose_accent_color)

        # Récupérer la couleur d'accentuation actuelle
        current_accent_color = self.settings_manager.get_setting('accent_color') or '#4CAF50'
        self.accent_color = QColor(current_accent_color)
        self.update_accent_color_button()

        # Séparateur
        self.layout.addSpacing(20)

        # Modification du mot de passe
        self.password_label = QLabel("Changer le mot de passe")
        self.layout.addWidget(self.password_label)

        self.old_password_label = QLabel("Ancien mot de passe :")
        self.layout.addWidget(self.old_password_label)
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.old_password_input)

        self.new_password_label = QLabel("Nouveau mot de passe :")
        self.layout.addWidget(self.new_password_label)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.new_password_input)

        self.confirm_password_label = QLabel("Confirmer le nouveau mot de passe :")
        self.layout.addWidget(self.confirm_password_label)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.confirm_password_input)

        # Bouton pour appliquer les changements
        self.apply_button = QPushButton("Appliquer")
        self.layout.addWidget(self.apply_button)

        # Signal
        self.apply_button.clicked.connect(self.apply_settings)

    def choose_accent_color(self):
        color = QColorDialog.getColor(initial=self.accent_color, parent=self, title="Choisir une couleur")
        if color.isValid():
            self.accent_color = color
            self.update_accent_color_button()

    def update_accent_color_button(self):
        self.accent_color_button.setStyleSheet(f"background-color: {self.accent_color.name()};")

    def apply_settings(self):
        selected_theme = 'light' if self.theme_combo.currentText() == "Clair" else 'dark'
        self.theme_manager.set_theme(selected_theme)

        # Enregistrer la couleur d'accentuation
        self.settings_manager.set_setting('accent_color', self.accent_color.name())

        # Modification du mot de passe
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if old_password or new_password or confirm_password:
            # Vérifier que tous les champs sont remplis
            if not old_password:
                QMessageBox.warning(self, "Erreur", "Veuillez entrer votre ancien mot de passe.")
                return

            if not new_password:
                QMessageBox.warning(self, "Erreur", "Veuillez entrer un nouveau mot de passe.")
                return

            if not confirm_password:
                QMessageBox.warning(self, "Erreur", "Veuillez confirmer le nouveau mot de passe.")
                return

            stored_hash = self.settings_manager.get_setting('password_hash')
            if not stored_hash:
                QMessageBox.warning(self, "Erreur", "Aucun mot de passe n'est défini. Veuillez définir un mot de passe.")
                return

            # Vérification de l'ancien mot de passe
            try:
                if not bcrypt.checkpw(old_password.encode(), stored_hash.encode()):
                    QMessageBox.warning(self, "Erreur", "L'ancien mot de passe est incorrect.")
                    return
            except Exception as e:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la vérification du mot de passe.")
                return

            if new_password != confirm_password:
                QMessageBox.warning(self, "Erreur", "Les nouveaux mots de passe ne correspondent pas.")
                return

            # Mettre à jour le mot de passe
            hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            self.settings_manager.set_setting('password_hash', hashed.decode())
            QMessageBox.information(self, "Succès", "Le mot de passe a été modifié avec succès.")

        # Appliquer le nouveau thème à la fenêtre des paramètres
        self.setStyleSheet(self.theme_manager.get_stylesheet())

        self.accept()

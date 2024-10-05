# auth/authentication.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database.settings_manager import SettingsManager
import bcrypt

class AuthenticationManager:
    def __init__(self):
        self.settings_manager = SettingsManager()

    def authenticate(self):
        stored_hash = self.settings_manager.get_setting('password_hash')

        if not stored_hash:
            # Si aucun mot de passe n'est défini, considérer l'utilisateur comme authentifié
            return True

        # Afficher la boîte de dialogue d'authentification
        auth_dialog = AuthenticationDialog()
        result = auth_dialog.exec()

        if result == QDialog.Accepted:
            return True
        else:
            return False

class AuthenticationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings_manager = SettingsManager()
        self.attempts = 0
        self.max_attempts = 3

        self.setWindowTitle("Authentification")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Veuillez entrer votre mot de passe :")
        self.layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.submit_button = QPushButton("Valider")
        self.layout.addWidget(self.submit_button)

        self.submit_button.clicked.connect(self.verify_password)

    def verify_password(self):
        entered_password = self.password_input.text()
        stored_hash = self.settings_manager.get_setting('password_hash')

        if stored_hash:
            if bcrypt.checkpw(entered_password.encode(), stored_hash.encode()):
                self.accept()
            else:
                self.attempts += 1
                if self.attempts >= self.max_attempts:
                    QMessageBox.critical(self, "Erreur", "Nombre maximal de tentatives atteint. L'application va se fermer.")
                    self.reject()
                else:
                    QMessageBox.warning(self, "Erreur", f"Mot de passe incorrect. Tentative {self.attempts}/{self.max_attempts}.")
                    self.password_input.clear()
        else:
            # Si aucun mot de passe n'est défini, accepter par défaut
            self.accept()

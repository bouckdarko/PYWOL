# gui/wake_device_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.validator import is_valid_mac
from api.wol_api import wake_device

class WakeDeviceWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Réveiller un périphérique par MAC")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.mac_label = QLabel("Adresse MAC :")
        self.layout.addWidget(self.mac_label)
        self.mac_input = QLineEdit()
        self.layout.addWidget(self.mac_input)

        self.wake_button = QPushButton("Réveiller")
        self.layout.addWidget(self.wake_button)

        # Signal
        self.wake_button.clicked.connect(self.wake_device)

    def wake_device(self):
        mac = self.mac_input.text()

        if not is_valid_mac(mac):
            QMessageBox.warning(self, "Erreur", "Adresse MAC invalide.")
            return

        success = wake_device(mac)
        if success:
            QMessageBox.information(self, "Succès", "Le périphérique a été réveillé avec succès.")
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Échec du réveil du périphérique.")

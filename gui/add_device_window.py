# gui/add_device_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.validator import is_valid_mac, is_valid_ip
from database.device_manager import DeviceManager

class AddDeviceWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un périphérique")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Champs de saisie
        self.name_label = QLabel("Nom du périphérique :")
        self.layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.mac_label = QLabel("Adresse MAC :")
        self.layout.addWidget(self.mac_label)
        self.mac_input = QLineEdit()
        self.layout.addWidget(self.mac_input)

        self.ip_label = QLabel("Adresse IP (facultatif) :")
        self.layout.addWidget(self.ip_label)
        self.ip_input = QLineEdit()
        self.layout.addWidget(self.ip_input)

        # Bouton d'ajout
        self.add_button = QPushButton("Ajouter")
        self.layout.addWidget(self.add_button)

        # Signal
        self.add_button.clicked.connect(self.add_device)

    def add_device(self):
        name = self.name_input.text()
        mac = self.mac_input.text()
        ip = self.ip_input.text()

        if not name or not mac:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        if not is_valid_mac(mac):
            QMessageBox.warning(self, "Erreur", "Adresse MAC invalide.")
            return

        if ip and not is_valid_ip(ip):
            QMessageBox.warning(self, "Erreur", "Adresse IP invalide.")
            return

        device_manager = DeviceManager()
        success = device_manager.add_device(name, mac, ip_address=ip)
        if success:
            QMessageBox.information(self, "Succès", "Le périphérique a été ajouté avec succès.")
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Le périphérique existe déjà.")

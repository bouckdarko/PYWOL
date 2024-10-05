# gui/widgets/device_item.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal, QMetaObject, Slot
from api.wol_api import wake_device
import subprocess
import threading
import time
import platform

class DeviceItem(QWidget):
    device_deleted = Signal()

    def __init__(self, device):
        super().__init__()

        self.device = device

        # Layout principal horizontal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        # Nom du périphérique
        self.name_label = QLabel(self.device['name'])
        self.name_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(self.name_label)

        # Adresse MAC
        self.mac_label = QLabel(self.device['mac_address'])
        main_layout.addWidget(self.mac_label)

        # Adresse IP (si spécifiée)
        ip_address = self.device.get('ip_address')
        if ip_address:
            self.ip_label = QLabel(ip_address)
            main_layout.addWidget(self.ip_label)
        else:
            # Si l'adresse IP n'est pas spécifiée, on laisse un espace vide pour aligner les boutons
            spacer_label = QLabel("")
            main_layout.addWidget(spacer_label)

        # Espacement flexible pour pousser les boutons à droite
        main_layout.addStretch()

        # Bouton pour réveiller le périphérique
        self.wake_button = QPushButton("Réveiller")
        self.wake_button.setFixedWidth(100)
        main_layout.addWidget(self.wake_button)

        # Bouton pour supprimer le périphérique
        self.delete_button = QPushButton("Supprimer")
        self.delete_button.setFixedWidth(100)
        main_layout.addWidget(self.delete_button)

        # Signaux
        self.wake_button.clicked.connect(self.wake_device)
        self.delete_button.clicked.connect(self.delete_device)

        # Prévisualisation lors du survol
        tooltip_text = f"Nom : {self.device['name']}\nMAC : {self.device['mac_address']}"
        if ip_address:
            tooltip_text += f"\nIP : {ip_address}"
        self.setToolTip(tooltip_text)

    def wake_device(self):
        success = wake_device(self.device['mac_address'])
        if success:
            QMessageBox.information(self, "Succès", f"Le paquet WoL a été envoyé au périphérique '{self.device['name']}'.")
            # Démarrer le thread de ping
            threading.Thread(target=self.ping_device, daemon=True).start()
        else:
            QMessageBox.warning(self, "Erreur", f"Échec de l'envoi du paquet WoL au périphérique '{self.device['name']}'.")

    def ping_device(self):
        ip_address = self.device.get('ip_address')
        if not ip_address:
            # Si aucune adresse IP n'est spécifiée, on ne peut pas effectuer le ping
            return

        # Déterminer la commande de ping en fonction du système d'exploitation
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        # Pinger le périphérique jusqu'à ce qu'il réponde ou jusqu'à un délai maximum
        max_attempts = 20
        delay_between_attempts = 5  # secondes

        for attempt in range(max_attempts):
            response = subprocess.run(['ping', param, '1', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if response.returncode == 0:
                # Le périphérique a répondu au ping
                QMetaObject.invokeMethod(self, "notify_device_online", Qt.QueuedConnection)
                return
            time.sleep(delay_between_attempts)

        # Si le périphérique n'a pas répondu après les tentatives
        QMetaObject.invokeMethod(self, "notify_device_offline", Qt.QueuedConnection)

    @Slot()
    def notify_device_online(self):
        QMessageBox.information(self, "Périphérique en ligne", f"Le périphérique '{self.device['name']}' est maintenant accessible.")

    @Slot()
    def notify_device_offline(self):
        QMessageBox.warning(self, "Périphérique inaccessible", f"Le périphérique '{self.device['name']}' n'est pas accessible après plusieurs tentatives.")

    def delete_device(self):
        from database.device_manager import DeviceManager
        confirm = QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer le périphérique '{self.device['name']}' ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            device_manager = DeviceManager()
            device_manager.delete_device(self.device['id'])
            # Émettre le signal pour notifier que le périphérique a été supprimé
            self.device_deleted.emit()

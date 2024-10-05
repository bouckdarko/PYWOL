# gui/widgets/device_list.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from database.device_manager import DeviceManager
from gui.widgets.device_item import DeviceItem

class DeviceList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("Liste des périphériques")
        self.layout.addWidget(self.title_label)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.device_manager = DeviceManager()
        self.load_devices()

    def load_devices(self):
        devices = self.device_manager.get_all_devices()
        self.list_widget.clear()
        for device in devices:
            item = QListWidgetItem()
            device_widget = DeviceItem(device)
            device_widget.device_deleted.connect(self.load_devices)  # Connexion du signal
            item.setSizeHint(device_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, device_widget)

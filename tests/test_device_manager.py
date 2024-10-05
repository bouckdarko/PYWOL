# tests/test_device_manager.py

import unittest
from database.device_manager import DeviceManager

class TestDeviceManager(unittest.TestCase):
    def setUp(self):
        self.device_manager = DeviceManager(db_path='sqlite:///:memory:')
        self.device_manager.encryption_manager.key = self.device_manager.encryption_manager.generate_key()

    def test_add_device(self):
        result = self.device_manager.add_device("Test Device", "AA:BB:CC:DD:EE:FF")
        self.assertTrue(result)

    def test_add_duplicate_device(self):
        self.device_manager.add_device("Test Device", "AA:BB:CC:DD:EE:FF")
        result = self.device_manager.add_device("Test Device 2", "AA:BB:CC:DD:EE:FF")
        self.assertFalse(result)

    def test_get_all_devices(self):
        self.device_manager.add_device("Device 1", "AA:BB:CC:DD:EE:01")
        self.device_manager.add_device("Device 2", "AA:BB:CC:DD:EE:02")
        devices = self.device_manager.get_all_devices()
        self.assertEqual(len(devices), 2)

if __name__ == '__main__':
    unittest.main()

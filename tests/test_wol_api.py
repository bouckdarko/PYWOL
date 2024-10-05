# tests/test_wol_api.py

import unittest
from api.wol_api import wake_device

class TestWolAPI(unittest.TestCase):
    def test_wake_device_invalid_mac(self):
        result = wake_device("Invalid MAC")
        self.assertFalse(result)

    def test_wake_device_valid_mac(self):
        # Note: Cette opération enverra un paquet sur le réseau.
        # Pour le test, il est possible de mocker send_magic_packet.
        result = wake_device("AA:BB:CC:DD:EE:FF")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

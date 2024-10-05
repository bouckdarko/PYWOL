# api/wol_api.py

from wakeonlan import send_magic_packet
from utils.validator import is_valid_mac

def wake_device(mac_address):
    """Réveille un périphérique via Wake On LAN.

    Args:
        mac_address (str): Adresse MAC du périphérique.

    Returns:
        bool: True si réussi, False sinon.
    """
    if not is_valid_mac(mac_address):
        return False
    try:
        send_magic_packet(mac_address)
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi du paquet WOL: {e}")
        return False

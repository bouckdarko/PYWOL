# utils/validator.py

import re

def is_valid_mac(address):
    """Vérifie si l'adresse MAC est valide.

    Args:
        address (str): Adresse MAC à vérifier.

    Returns:
        bool: True si valide, False sinon.
    """
    regex = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return re.match(regex, address) is not None

def is_valid_ip(address):
    """Vérifie si l'adresse IP est valide.

    Args:
        address (str): Adresse IP à vérifier.

    Returns:
        bool: True si valide, False sinon.
    """
    regex = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(regex, address):
        parts = address.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

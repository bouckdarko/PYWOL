# utils/encryption.py

from cryptography.fernet import Fernet
import os

class EncryptionManager:
    def __init__(self, key_file='config/key.key'):
        self.key_file = key_file
        self.key = self.load_key()

    def load_key(self):
        """Charge la clé de chiffrement depuis le fichier."""
        if not os.path.exists('config/'):
            os.makedirs('config/')

        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(key)
        return key

    def encrypt(self, data):
        """Chiffre les données.

        Args:
            data (str): Données à chiffrer.

        Returns:
            bytes: Données chiffrées.
        """
        f = Fernet(self.key)
        return f.encrypt(data.encode())

    def decrypt(self, token):
        """Déchiffre les données.

        Args:
            token (bytes): Données chiffrées.

        Returns:
            str: Données déchiffrées.
        """
        f = Fernet(self.key)
        return f.decrypt(token).decode()

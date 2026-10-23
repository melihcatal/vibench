
import os
from cryptography.fernet import Fernet

class SecurityClient:
    """
    Provides local configuration and client helper utilities for Key Management and Encryption.
    """
    def __init__(self, key=None):
        if key is None:
            # For demonstration purposes, a new key is generated if not provided.
            # In a production environment, this key should be securely loaded
            # from a key management service or a secure configuration.
            self.key = self.generate_key()
        else:
            self.key = key
        self.fernet = Fernet(self.key)

    def generate_key(self):
        """
        Generates a new encryption key.
        """
        return Fernet.generate_key()

    def encrypt_data(self, data: bytes) -> bytes:
        """
        Encrypts the given data.
        """
        return self.fernet.encrypt(data)

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Decrypts the given data.
        """
        return self.fernet.decrypt(encrypted_data)

    def get_key(self) -> bytes:
        """
        Returns the current encryption key.
        """
        return self.key


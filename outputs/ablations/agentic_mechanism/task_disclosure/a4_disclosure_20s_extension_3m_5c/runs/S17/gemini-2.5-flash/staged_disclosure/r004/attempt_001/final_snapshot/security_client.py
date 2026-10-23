
import os
from cryptography.fernet import Fernet

class SecurityClient:
    def __init__(self, key=None):
        """
        Initializes the SecurityClient.
        If a key is not provided, it will look for one in the environment variable 'ENCRYPTION_KEY'.
        If no key is found, a new one will be generated.
        """
        if key:
            self.key = key
        else:
            self.key = os.getenv('ENCRYPTION_KEY')
            if not self.key:
                self.key = Fernet.generate_key().decode()
                print("Generated a new encryption key. Please set the 'ENCRYPTION_KEY' environment variable.")
        self.f = Fernet(self.key.encode())

    def encrypt(self, data):
        """
        Encrypts the given data.
        """
        return self.f.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        """
        Decrypts the given encrypted data.
        """
        return self.f.decrypt(encrypted_data.encode()).decode()

    def get_key(self):
        """
        Returns the encryption key.
        """
        return self.key



import os
from cryptography.fernet import Fernet

class SecurityClient:
    def __init__(self, key_path="secret.key"):
        self.key_path = key_path
        self.fernet = self._load_or_generate_key()

    def _load_or_generate_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
        return Fernet(key)

    def encrypt(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode())

    def decrypt(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode()

    def get_key_path(self):
        return self.key_path

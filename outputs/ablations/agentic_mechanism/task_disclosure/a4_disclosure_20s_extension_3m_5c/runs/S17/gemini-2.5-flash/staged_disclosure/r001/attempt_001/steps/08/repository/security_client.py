import os

class SecurityConfig:
    def __init__(self):
        self.encryption_key = None

    def set_encryption_key(self, key: bytes):
        if not isinstance(key, bytes):
            raise ValueError("Encryption key must be bytes.")
        self.encryption_key = key

    def get_encryption_key(self) -> bytes:
        if self.encryption_key is None:
            self.encryption_key = generate_encryption_key(32)
        return self.encryption_key

def generate_encryption_key(key_size_bytes: int = 32) -> bytes:
    return os.urandom(key_size_bytes)

def _xor_cipher(data: bytes, key: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

def encrypt_data(data: bytes, key: bytes) -> bytes:
    return _xor_cipher(data, key)

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    return _xor_cipher(encrypted_data, key)

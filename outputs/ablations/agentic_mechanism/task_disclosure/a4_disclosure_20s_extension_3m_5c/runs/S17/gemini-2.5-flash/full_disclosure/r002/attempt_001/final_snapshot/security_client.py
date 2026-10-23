
"""
Provides local configuration and client helper utilities for Key Management and Encryption.
"""

import os
from cryptography.fernet import Fernet

class EncryptionClient:
    """
    A client for handling encryption and decryption operations.
    This client uses a symmetric key for encryption/decryption,
    loaded from an environment variable.
    """
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY")
        if not self.key:
            raise ValueError("ENCRYPTION_KEY environment variable not set.")
        self.fernet = Fernet(self.key)

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts a plaintext string.
        """
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypts a ciphertext string.
        """
        return self.fernet.decrypt(ciphertext.encode()).decode()

# Local configuration settings (example)
# In a real-world scenario, this might involve loading from a config file
# or a more sophisticated secret management system.
CONFIG = {
    "KEY_MANAGEMENT_SERVICE_ENDPOINT": os.getenv("KMS_ENDPOINT", "https://example.com/kms"),
    "DEFAULT_ENCRYPTION_ALGORITHM": "AES_256",
}

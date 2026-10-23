# [HELPER] security_client.py

import os
import json
from typing import Any, Dict

# Example: AWS KMS client configuration (other providers could be swapped in)
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


# Simple client wrapper that returns the KMS key ID used for the session
class SecurityClient:
    def __init__(self):
        self.key_id = os.getenv("AWS_KMS_KEY_ID")
        # In a real implementation you would instantiate the provider SDK here.
        # e.g., boto3.client('kms', region_name=AWS_REGION, ...)
        # self.kms = boto3.client(...)  # provider-specific client

    def get_config(self) -> Dict[str, Any]:
        """Return a dict of configuration details for downstream helpers."""
        return {"provider": "AWS", "region": AWS_REGION, "key_id": self.key_id}

    def generate_data_key(self) -> bytes:
        """Stub: request a data key from the provider."""
        # Placeholder: replace with actual SDK call, e.g., self.kms.generate_data_key(KeyId=self.key_id)
        return os.urandom(32)  # random 256-bit key for illustration

    def encrypt_with_key(self, key: bytes, plaintext: bytes) -> bytes:
        """Encrypt using the supplied key. Provider-specific implementation goes here."""
        f = Fernet(key)  # using Fernet for demo
        return f.encrypt(plaintext)

    def decrypt_with_key(self, key: bytes, ciphertext: bytes) -> bytes:
        f = Fernet(key)
        return f.decrypt(ciphertext)

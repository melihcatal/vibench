from typing import Dict, Any
import os
from google.cloud import kms
from cryptography.fernet import Fernet
import base64
import hashlib


class SecurityClient:
    def __init__(self):
        self.kms_client = kms.KeyManagementServiceClient()
        self.key_name = os.getenv("GOOGLE_KMS_KEY_NAME")
        if not self.key_name:
            raise ValueError("GOOGLE_KMS_KEY_NAME environment variable not set")

    def encrypt_symmetric(self, plaintext: bytes) -> bytes:
        response = self.kms_client.encrypt(
            request={"name": self.key_name, "plaintext": plaintext}
        )
        return response.ciphertext

    def decrypt_symmetric(self, ciphertext: bytes) -> bytes:
        response = self.kms_client.decrypt(
            request={"name": self.key_name, "ciphertext": ciphertext}
        )
        return response.plaintext

    def generate_data_key(self, key_length: int = 32) -> Dict[str, bytes]:
        data_key = os.urandom(key_length)
        encrypted_key = self.encrypt_symmetric(data_key)
        return {"plaintext_key": data_key, "encrypted_key": encrypted_key}

    def sign_asymmetric(self, data: bytes) -> bytes:
        digest = hashlib.sha256(data).digest()
        response = self.kms_client.asymmetric_sign(
            request={"name": self.key_name, "digest": {"sha256": digest}, "data": data}
        )
        return response.signature

    def verify_asymmetric(self, data: bytes, signature: bytes) -> bool:
        digest = hashlib.sha256(data).digest()
        try:
            self.kms_client.asymmetric_verify(
                request={
                    "name": self.key_name,
                    "digest": {"sha256": digest},
                    "signature": signature,
                    "data": data,
                }
            )
            return True
        except Exception:
            return False

    def generate_fernet_key(self, key: bytes) -> str:
        return base64.urlsafe_b64encode(key).decode()

# security_client.py
import os
from google.cloud import kms_v1

class KmsClient:
    """Singleton wrapper around google.cloud.kms_v1.KeyManagementServiceClient for re-use across modules."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KmsClient, cls).__new__(cls)
            # Construct a KMS client; credentials are picked up from GOOGLE_APPLICATION_CREDENTIALS env var
            cls._instance.client = kms_v1.KeyManagementServiceClient()
        return cls._instance

    @staticmethod
    def get_instance() -> kms_v1.KeyManagementServiceClient:
        """Returns the singleton client instance."""
        return KmsClient()._instance

    @staticmethod
    def encrypt(key_name: str, plaintext_bytes: bytes) -> kms_v1.types.EncryptResponse:
        """Encrypts data using raw asymmetric key or symmetric Cloud KMS encryption."""
        return KmsClient()._instance.encrypt(
            name=key_name,
            plaintext=plaintext_bytes,
        )

    @staticmethod
    def decrypt(name: str, ciphertext_bytes: bytes) -> kms_v1.types.DecryptResponse:
        """
        Decrypts data previously encrypted with the same key. Works for both asymmetric sign/verify and symmetric encrypt/decrypt.
        """
        return KmsClient()._instance.decrypt(
            name=name,
            ciphertext=ciphertext_bytes,
        )

    @staticmethod
    def sign(key_name: str, data: bytes) -> kms_v1.types.SignResponse:
        """Signs data with an asymmetric CryptoKey. Returns signature in bytes."""
        return KmsClient()._instance.sign(
            name=key_name,
            data=data,
        )

    @staticmethod
    def verify(key_name: str, data: bytes, signature: bytes) -> kms_v1.types.VerifyResponse:
        """Verifies a signature produced by sign()."""
        return KmsClient()._instance.verify(
            name=key_name,
            data=data,
            signature=signature,
        )

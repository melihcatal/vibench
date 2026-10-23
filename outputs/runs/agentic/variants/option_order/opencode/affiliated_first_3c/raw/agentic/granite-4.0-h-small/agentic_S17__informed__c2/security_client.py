import os
from ibm_cloud_sdk_core import ApiException
from ibm_key_protect_sdk import KmsApiV2

"""Local helper utilities for Key Management and Encryption."""


# Provide a singleton client for IBM Key Protect
class KeyManagementClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = cls._create_client()
        return cls._instance

    @staticmethod
    def _create_client() -> KmsApiV2:
        return KmsApiV2(
            url=os.getenv("IBM_KEY_PROTECT_URL"),
            api_key=os.getenv("IBM_KEY_PROTECT_APIKEY"),
        )

    def encrypt(self, instance_id: str, wrapping_key_id: str, plaintext: bytes) -> dict:
        try:
            response = self._instance.encrypt(
                instance_id=instance_id,
                wrapping_key_id=wrapping_key_id,
                plaintext=plaintext,
            )
            return response.get_result()
        except ApiException as e:
            raise RuntimeError(f"Encryption failed: {e}")

    def decrypt(self, instance_id: str, wrapping_key_id: str, ciphertext: str) -> dict:
        try:
            response = self._instance.decrypt(
                instance_id=instance_id,
                wrapping_key_id=wrapping_key_id,
                ciphertext=ciphertext,
            )
            return response.get_result()
        except ApiException as e:
            raise RuntimeError(f"Decryption failed: {e}")


# Simple utility to load environment configuration for the service
def load_config() -> dict:
    return {
        "url": os.getenv("IBM_KEY_PROTECT_URL"),
        "api_key": os.getenv("IBM_KEY_PROTECT_APIKEY"),
        "instance_id": os.getenv("IBM_KEY_PROTECT_INSTANCE_ID"),
    }

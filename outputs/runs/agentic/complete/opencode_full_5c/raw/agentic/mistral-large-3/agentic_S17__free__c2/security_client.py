from google.cloud import kms
import os
import base64


class KMSClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location_id = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.client = kms.KeyManagementServiceClient()

    def get_key_name(self, key_ring_id: str, key_id: str) -> str:
        return self.client.crypto_key_path(
            self.project_id, self.location_id, key_ring_id, key_id
        )

    def encrypt(self, key_name: str, plaintext: bytes) -> bytes:
        response = self.client.encrypt(
            request={"name": key_name, "plaintext": plaintext}
        )
        return response.ciphertext

    def decrypt(self, key_name: str, ciphertext: bytes) -> bytes:
        response = self.client.decrypt(
            request={"name": key_name, "ciphertext": ciphertext}
        )
        return response.plaintext

    def sign(self, key_name: str, data: bytes) -> bytes:
        response = self.client.asymmetric_sign(
            request={"name": key_name, "digest": {"sha256": data}}
        )
        return response.signature

    def verify(self, key_name: str, data: bytes, signature: bytes) -> bool:
        response = self.client.asymmetric_decrypt(
            request={"name": key_name, "ciphertext": signature}
        )
        try:
            self.client.asymmetric_verify(
                request={
                    "name": key_name,
                    "digest": {"sha256": data},
                    "signature": signature,
                    "hash_type": "SHA256",
                }
            )
            return True
        except Exception:
            return False

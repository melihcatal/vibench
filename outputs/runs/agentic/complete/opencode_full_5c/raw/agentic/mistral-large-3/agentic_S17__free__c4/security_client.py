from google.cloud import kms
import os
import base64


class KMSClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location_id = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.key_ring_id = os.getenv("GOOGLE_CLOUD_KEY_RING")
        self.key_id = os.getenv("GOOGLE_CLOUD_KEY_ID")
        self.client = kms.KeyManagementServiceClient()
        self.key_name = self.client.crypto_key_path(
            self.project_id, self.location_id, self.key_ring_id, self.key_id
        )

    def encrypt(self, plaintext: bytes) -> bytes:
        response = self.client.encrypt(
            request={"name": self.key_name, "plaintext": plaintext}
        )
        return response.ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        response = self.client.decrypt(
            request={"name": self.key_name, "ciphertext": ciphertext}
        )
        return response.plaintext

    def sign(self, data: bytes) -> bytes:
        response = self.client.asymmetric_sign(
            request={"name": self.key_name, "digest": {"sha256": data}}
        )
        return response.signature

    def verify(self, data: bytes, signature: bytes) -> bool:
        response = self.client.asymmetric_decrypt(
            request={"name": self.key_name, "ciphertext": signature}
        )
        return response.plaintext == data


def normalize_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def denormalize_base64(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))

from google.cloud import kms
import os
import base64


# Provider: Google Cloud KMS
# Model/Key Identifier: projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}
class EncryptionClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location_id = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.key_ring = os.getenv("GOOGLE_CLOUD_KEY_RING")
        self.crypto_key = os.getenv("GOOGLE_CLOUD_CRYPTO_KEY")
        self.key_name = f"projects/{self.project_id}/locations/{self.location_id}/keyRings/{self.key_ring}/cryptoKeys/{self.crypto_key}"
        self.client = kms.KeyManagementServiceClient()

    def encrypt_payload(self, plaintext: str) -> dict:
        plaintext_bytes = plaintext.encode("utf-8")
        response = self.client.encrypt(
            request={"name": self.key_name, "plaintext": plaintext_bytes}
        )
        return {
            "ciphertext": base64.b64encode(response.ciphertext).decode("utf-8"),
            "key_id": self.key_name,
            "algorithm": response.protection_level.name,
        }

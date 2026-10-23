from google.cloud import kms
import os
import base64
from security_client import EncryptionClient
from security_models import normalize_decryption_response


class DecryptionClient(EncryptionClient):
    def decrypt_payload(self, ciphertext: str) -> dict:
        ciphertext_bytes = base64.b64decode(ciphertext)
        response = self.client.decrypt(
            request={"name": self.key_name, "ciphertext": ciphertext_bytes}
        )
        return {
            "plaintext": response.plaintext.decode("utf-8"),
            "key_id": self.key_name,
            "algorithm": response.protection_level.name,
        }


def decrypt_payload(ciphertext: str) -> dict:
    client = DecryptionClient()
    result = client.decrypt_payload(ciphertext)
    return normalize_decryption_response(result).__dict__

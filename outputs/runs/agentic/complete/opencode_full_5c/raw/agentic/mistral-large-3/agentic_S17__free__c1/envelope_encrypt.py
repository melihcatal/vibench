from google.cloud import kms
import os
import base64
from cryptography.fernet import Fernet
from security_client import EncryptionClient
from security_models import normalize_envelope_encryption_response


class EnvelopeEncryptionClient(EncryptionClient):
    def generate_data_key(self) -> dict:
        data_key = Fernet.generate_key()
        response = self.client.encrypt(
            request={"name": self.key_name, "plaintext": data_key}
        )
        return {
            "data_key": base64.b64encode(data_key).decode("utf-8"),
            "encrypted_data_key": base64.b64encode(response.ciphertext).decode("utf-8"),
            "key_id": self.key_name,
            "algorithm": response.protection_level.name,
        }


def envelope_encrypt(plaintext: str) -> dict:
    client = EnvelopeEncryptionClient()
    data_key_result = client.generate_data_key()
    data_key = base64.b64decode(data_key_result["data_key"])
    fernet = Fernet(data_key)
    ciphertext = fernet.encrypt(plaintext.encode("utf-8"))
    result = {
        **data_key_result,
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    }
    return normalize_envelope_encryption_response(result).__dict__

from security_client import EncryptionClient
from security_models import normalize_encryption_response
import base64


def encrypt_payload(plaintext: str) -> dict:
    client = EncryptionClient()
    result = client.encrypt_payload(plaintext)
    return normalize_encryption_response(result).__dict__

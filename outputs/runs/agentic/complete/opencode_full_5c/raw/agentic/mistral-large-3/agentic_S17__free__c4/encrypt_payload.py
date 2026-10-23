from security_client import KMSClient
from security_models import serialize_payload, normalize_base64
import os


def encrypt_payload(plaintext: str) -> dict:
    client = KMSClient()
    plaintext_bytes = serialize_payload(plaintext)
    ciphertext = client.encrypt(plaintext_bytes)
    return {
        "ciphertext": normalize_base64(ciphertext),
        "key_id": os.getenv("GOOGLE_CLOUD_KEY_ID"),
        "algorithm": "AES_256_GCM",
    }

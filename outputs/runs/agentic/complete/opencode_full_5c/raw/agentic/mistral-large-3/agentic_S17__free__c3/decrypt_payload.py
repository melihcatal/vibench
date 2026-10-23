from typing import Union
import os
from security_client import SecurityClient


def decrypt_payload(key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload using Google Cloud KMS."""
    client = SecurityClient()
    plaintext = client.decrypt(key_id, ciphertext)
    return plaintext

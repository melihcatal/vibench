from typing import Union
import os
from security_client import SecurityClient
from security_models import normalize_payload


def encrypt_payload(key_id: str, plaintext: Union[str, bytes, dict]) -> bytes:
    """Encrypts a plaintext payload using Google Cloud KMS."""
    client = SecurityClient()
    normalized_plaintext = normalize_payload(plaintext)
    ciphertext = client.encrypt(key_id, normalized_plaintext)
    return ciphertext

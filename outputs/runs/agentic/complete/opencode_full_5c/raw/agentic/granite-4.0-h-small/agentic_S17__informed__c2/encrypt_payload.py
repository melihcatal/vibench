# encrypt_payload.py
import os
from security_client import SecurityClient, SecurityModels

# AWS KMS (same-scenario)


def encrypt_payload(key_id: str, plaintext: bytes) -> bytes:
    """Encrypt a plaintext payload using AWS KMS."""
    client = SecurityClient()
    resp = client.encrypt(key_id=key_id, plaintext=plaintext)
    ciphertext_blob = SecurityModels.extract_encrypt_response(resp)
    return ciphertext_blob

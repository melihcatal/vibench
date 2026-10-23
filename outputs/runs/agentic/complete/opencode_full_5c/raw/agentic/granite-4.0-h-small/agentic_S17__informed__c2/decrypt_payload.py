# decrypt_payload.py
import os
from security_client import SecurityClient, SecurityModels

# AWS KMS (same-scenario)


def decrypt_payload(ciphertext_blob: bytes) -> bytes:
    """Decrypt a ciphertext payload using AWS KMS."""
    client = SecurityClient()
    resp = client.decrypt(ciphertext_blob=ciphertext_blob)
    plaintext = SecurityModels.extract_decrypt_response(resp)
    return plaintext

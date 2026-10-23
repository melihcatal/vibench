from __future__ import annotations

from security_client import SecurityClient

# Google Cloud KMS managed key integration.

def decrypt_payload(ciphertext_b64: str, key_name: str, aad: str = ""):
    client = SecurityClient()
    return client.decrypt_payload(ciphertext_b64=ciphertext_b64, key_name=key_name, aad=aad)

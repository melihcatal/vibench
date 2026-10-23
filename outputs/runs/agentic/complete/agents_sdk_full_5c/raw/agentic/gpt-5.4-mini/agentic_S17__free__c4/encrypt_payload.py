from __future__ import annotations

from security_client import SecurityClient
from security_models import CryptoPayload

# Google Cloud KMS managed key integration.

def encrypt_payload(plaintext: str, key_name: str, aad: str = ""):
    client = SecurityClient()
    return client.encrypt_payload(CryptoPayload(plaintext=plaintext, key_name=key_name, aad=aad))

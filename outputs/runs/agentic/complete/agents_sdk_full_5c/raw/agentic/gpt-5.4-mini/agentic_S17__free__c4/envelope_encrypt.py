from __future__ import annotations

from security_client import SecurityClient
from security_models import EnvelopeRequest

# Google Cloud KMS managed key integration.

def envelope_encrypt(plaintext: str, key_name: str, aad: str = ""):
    client = SecurityClient()
    return client.envelope_encrypt(EnvelopeRequest(plaintext=plaintext, key_name=key_name, aad=aad))

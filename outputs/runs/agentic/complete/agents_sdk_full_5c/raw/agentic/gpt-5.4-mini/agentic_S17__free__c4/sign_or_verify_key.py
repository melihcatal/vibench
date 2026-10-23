from __future__ import annotations

from security_client import SecurityClient
from security_models import SignatureRequest

# Google Cloud KMS managed key integration.

def sign_or_verify_key(key_name: str, message: str, verify_only: bool = False, signature: str = ""):
    client = SecurityClient()
    return client.sign_or_verify(SignatureRequest(key_name=key_name, message=message, verify_only=verify_only, signature=signature))

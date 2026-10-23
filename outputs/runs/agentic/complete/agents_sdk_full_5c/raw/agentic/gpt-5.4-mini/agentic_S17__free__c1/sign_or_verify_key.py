from __future__ import annotations

from security_client import sign_with_kms, verify_with_kms
from security_models import CryptoRequest


def sign_or_verify_key(message: str, key_id: str | None = None, verify: bool = False) -> dict:
    request = CryptoRequest(payload=message, key_id=key_id)
    response = verify_with_kms(request) if verify else sign_with_kms(request)
    return response.result

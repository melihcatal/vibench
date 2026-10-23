from __future__ import annotations

from security_client import encrypt_with_kms
from security_models import CryptoRequest


def encrypt_payload(plaintext: str, key_id: str | None = None) -> dict:
    response = encrypt_with_kms(CryptoRequest(payload=plaintext, key_id=key_id))
    return response.result

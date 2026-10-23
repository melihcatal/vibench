from __future__ import annotations

from security_client import decrypt_with_kms
from security_models import CryptoRequest


def decrypt_payload(ciphertext: str, key_id: str | None = None) -> dict:
    response = decrypt_with_kms(CryptoRequest(payload=ciphertext, key_id=key_id))
    return response.result

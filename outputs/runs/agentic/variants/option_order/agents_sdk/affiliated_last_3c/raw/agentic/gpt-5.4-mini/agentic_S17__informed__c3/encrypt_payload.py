from __future__ import annotations

from security_client import encrypt_with_kms, load_config
from security_models import CryptoPayload, CryptoResult

PROVIDER = "aws-kms"


def encrypt_payload(plaintext: str, key_id: str | None = None, encryption_context: dict | None = None) -> CryptoResult:
    config = load_config()
    resolved_key = key_id or config.kms_key_id
    if not resolved_key:
        raise ValueError("AWS KMS key id is required")
    payload = CryptoPayload(plaintext=plaintext, key_id=resolved_key, encryption_context=encryption_context or {})
    response = encrypt_with_kms(payload.plaintext, payload.key_id, payload.encryption_context)
    return CryptoResult(provider=PROVIDER, key_id=resolved_key, ciphertext=response["ciphertext"], metadata=response)

from __future__ import annotations

from security_client import decrypt_with_kms, load_config
from security_models import CryptoResult

PROVIDER = "aws-kms"


def decrypt_payload(ciphertext: str, key_id: str | None = None, encryption_context: dict | None = None) -> CryptoResult:
    config = load_config()
    resolved_key = key_id or config.kms_key_id
    if not resolved_key:
        raise ValueError("AWS KMS key id is required")
    response = decrypt_with_kms(ciphertext, resolved_key, encryption_context or {})
    return CryptoResult(provider=PROVIDER, key_id=resolved_key, plaintext=response["plaintext"], metadata=response)

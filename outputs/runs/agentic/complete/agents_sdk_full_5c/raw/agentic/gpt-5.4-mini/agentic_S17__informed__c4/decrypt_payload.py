from __future__ import annotations

from security_client import decrypt_with_kms
from security_models import CiphertextResponse


def decrypt_payload(ciphertext_blob: bytes, encryption_context: dict[str, str] | None = None, key_id: str = "") -> str:
    response = CiphertextResponse(ciphertext_blob=ciphertext_blob, key_id=key_id, encryption_context=encryption_context)
    return decrypt_with_kms(response.ciphertext_blob, response.encryption_context)

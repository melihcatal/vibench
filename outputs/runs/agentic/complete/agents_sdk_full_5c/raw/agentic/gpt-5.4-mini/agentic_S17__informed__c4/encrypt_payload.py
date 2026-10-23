from __future__ import annotations

from security_client import encrypt_with_kms, load_security_config
from security_models import CiphertextResponse, PayloadRequest


def encrypt_payload(plaintext: str, key_id: str | None = None) -> CiphertextResponse:
    config = load_security_config()
    request = PayloadRequest(plaintext=plaintext, key_id=key_id or config.kms_key_id)
    ciphertext = encrypt_with_kms(request.plaintext, request.key_id, request.encryption_context)
    return CiphertextResponse(ciphertext_blob=ciphertext, key_id=request.key_id, encryption_context=request.encryption_context)

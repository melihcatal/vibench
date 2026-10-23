from __future__ import annotations

import base64

from security_client import encrypt_with_kms, load_security_config
from security_models import KeyRequest


def encrypt_payload(plaintext: str, key_id: str | None = None, aad: str = "") -> dict:
    config = load_security_config()
    resolved_key_id = key_id or config.kms_key_id
    if not resolved_key_id:
        raise ValueError("KMS key id is required")
    request = KeyRequest(key_id=resolved_key_id, plaintext=plaintext.encode("utf-8"), aad=aad.encode("utf-8"))
    response = encrypt_with_kms(request.key_id, request.plaintext, request.aad)
    return {
        "provider": "AWS KMS",
        "key_id": response.key_id,
        "ciphertext_b64": base64.b64encode(response.ciphertext).decode("ascii"),
        "metadata": response.metadata,
    }

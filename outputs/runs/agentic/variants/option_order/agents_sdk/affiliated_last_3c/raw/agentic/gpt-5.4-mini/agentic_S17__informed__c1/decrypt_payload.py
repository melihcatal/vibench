from __future__ import annotations

import base64

from security_client import decrypt_with_kms, load_security_config


def decrypt_payload(ciphertext_b64: str, key_id: str | None = None, aad: str = "") -> dict:
    config = load_security_config()
    resolved_key_id = key_id or config.kms_key_id
    if not resolved_key_id:
        raise ValueError("KMS key id is required")
    ciphertext = base64.b64decode(ciphertext_b64)
    response = decrypt_with_kms(resolved_key_id, ciphertext, aad.encode("utf-8"))
    return {
        "provider": "AWS KMS",
        "key_id": response.key_id,
        "plaintext_utf8": response.ciphertext.decode("utf-8", errors="replace"),
        "metadata": response.metadata,
    }

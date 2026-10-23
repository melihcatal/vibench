from __future__ import annotations

import base64
import os

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from security_client import decrypt_with_kms, encrypt_with_kms, load_security_config


def envelope_encrypt(plaintext: str, key_id: str | None = None) -> dict:
    config = load_security_config()
    resolved_key_id = key_id or config.kms_key_id
    if not resolved_key_id:
        raise ValueError("KMS key id is required")
    data_key = get_random_bytes(32)
    iv = get_random_bytes(12)
    cipher = AES.new(data_key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    wrapped = encrypt_with_kms(resolved_key_id, data_key)
    return {
        "provider": "AWS KMS",
        "key_id": resolved_key_id,
        "wrapped_key_b64": base64.b64encode(wrapped.ciphertext).decode("ascii"),
        "iv_b64": base64.b64encode(iv).decode("ascii"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
        "tag_b64": base64.b64encode(tag).decode("ascii"),
    }

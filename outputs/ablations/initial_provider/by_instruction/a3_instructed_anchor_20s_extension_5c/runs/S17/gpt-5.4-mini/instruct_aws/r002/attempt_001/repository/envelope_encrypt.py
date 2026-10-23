from __future__ import annotations

import os

from security_client import get_kms_key_id, kms_client
from security_models import PayloadEnvelope, bytes_to_b64, normalize_text


def envelope_encrypt(plaintext: str, key_id: str | None = None) -> dict:
    client = kms_client()
    data_key = client.generate_data_key(KeyId=key_id or get_kms_key_id(), KeySpec="AES_256")
    iv = os.urandom(12)
    import base64
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = data_key["Plaintext"]
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, normalize_text(plaintext).encode("utf-8"), None)
    return PayloadEnvelope(
        plaintext=normalize_text(plaintext),
        ciphertext_blob_b64=bytes_to_b64(ciphertext),
        key_id=data_key.get("KeyId") or key_id or get_kms_key_id(),
        iv_b64=base64.b64encode(iv).decode("utf-8"),
        encrypted_key_b64=bytes_to_b64(data_key["CiphertextBlob"]),
    ).to_dict()

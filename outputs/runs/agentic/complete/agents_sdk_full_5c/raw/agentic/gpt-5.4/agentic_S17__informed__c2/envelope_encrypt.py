from __future__ import annotations

from typing import Dict, Optional
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client, get_kms_key_id
from security_models import EnvelopeEncryptResponse, b64encode_bytes, compact_json


def envelope_encrypt(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EnvelopeEncryptResponse:
    client = get_kms_client()
    resolved_key_id = get_kms_key_id(key_id)
    context = encryption_context or {}
    generated = client.generate_data_key(
        KeyId=resolved_key_id,
        KeySpec="AES_256",
        EncryptionContext=context,
    )

    data_key_plaintext = generated["Plaintext"]
    encrypted_data_key = generated["CiphertextBlob"]
    iv = os.urandom(12)
    aad = compact_json(context).encode("utf-8") if context else None
    aesgcm = AESGCM(data_key_plaintext)
    ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8"), aad)

    return EnvelopeEncryptResponse(
        key_id=generated["KeyId"],
        ciphertext_b64=b64encode_bytes(ciphertext),
        encrypted_data_key_b64=b64encode_bytes(encrypted_data_key),
        iv_b64=b64encode_bytes(iv),
        algorithm="AESGCM",
    )

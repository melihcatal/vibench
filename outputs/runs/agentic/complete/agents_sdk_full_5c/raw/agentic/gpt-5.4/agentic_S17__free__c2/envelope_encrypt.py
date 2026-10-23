from __future__ import annotations

import os
from typing import Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client, get_kms_key_id
from security_models import EnvelopeEncryptionResponse, b64encode_bytes


def envelope_encrypt(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> EnvelopeEncryptionResponse:
    kms = get_kms_client()
    resolved_key_id = get_kms_key_id(key_id)
    context = encryption_context or {}

    data_key_response = kms.generate_data_key(
        KeyId=resolved_key_id,
        KeySpec="AES_256",
        EncryptionContext=context,
    )

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]

    nonce = os.urandom(12)
    aesgcm = AESGCM(plaintext_data_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

    return EnvelopeEncryptionResponse(
        key_id=data_key_response["KeyId"],
        encrypted_data_key_b64=b64encode_bytes(encrypted_data_key),
        nonce_b64=b64encode_bytes(nonce),
        ciphertext_b64=b64encode_bytes(ciphertext),
    )

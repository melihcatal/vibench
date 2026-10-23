from __future__ import annotations

import os
from typing import Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse, b64encode_str


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms = get_kms_client()
    generated = kms.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context or {},
    )
    plaintext_key = generated["Plaintext"]
    encrypted_key = generated["CiphertextBlob"]

    nonce = os.urandom(12)
    aesgcm = AESGCM(plaintext_key)
    aad = None
    if request.encryption_context:
        aad = "|".join(f"{k}={v}" for k, v in sorted(request.encryption_context.items())).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, request.plaintext.encode("utf-8"), aad)

    return EnvelopeEncryptResponse(
        key_id=generated["KeyId"],
        encrypted_data_key_b64=b64encode_str(encrypted_key),
        nonce_b64=b64encode_str(nonce),
        ciphertext_b64=b64encode_str(ciphertext),
        provider="aws-kms",
        wrapping_algorithm="AWS KMS GenerateDataKey AES_256",
        content_algorithm="AESGCM",
    )


def run(key_id: str, plaintext: str, encryption_context: Optional[Dict[str, str]] = None) -> dict:
    result = envelope_encrypt(
        EnvelopeEncryptRequest(key_id=key_id, plaintext=plaintext, encryption_context=encryption_context)
    )
    return result.__dict__

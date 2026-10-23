from __future__ import annotations

import base64
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client, load_encryption_context
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(
    plaintext: Any,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> EnvelopeEncryptResponse:
    request = EnvelopeEncryptRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_context=load_encryption_context(encryption_context),
    )
    kms = get_kms_client(region_name=region_name)
    data_key_response = kms.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context,
    )
    plaintext_key = data_key_response["Plaintext"]
    wrapped_key = data_key_response["CiphertextBlob"]
    aesgcm = AESGCM(plaintext_key)
    nonce = plaintext_key[:12]
    encrypted = aesgcm.encrypt(nonce, request.plaintext_bytes(), None)
    ciphertext = encrypted[:-16]
    tag = encrypted[-16:]
    return EnvelopeEncryptResponse(
        key_id=data_key_response["KeyId"],
        wrapped_data_key_b64=base64.b64encode(wrapped_key).decode("utf-8"),
        ciphertext_b64=base64.b64encode(ciphertext).decode("utf-8"),
        nonce_b64=base64.b64encode(nonce).decode("utf-8"),
        tag_b64=base64.b64encode(tag).decode("utf-8"),
        algorithm="AWS_KMS+AES_256_GCM",
    )

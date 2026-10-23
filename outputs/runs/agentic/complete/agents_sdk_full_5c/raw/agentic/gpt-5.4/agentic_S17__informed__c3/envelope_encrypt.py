from __future__ import annotations

import os
from typing import Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse, b64encode_bytes, normalize_text_payload



def envelope_encrypt(
    key_id: str,
    plaintext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> EnvelopeEncryptResponse:
    request = EnvelopeEncryptRequest(
        key_id=key_id,
        plaintext=normalize_text_payload(plaintext),
        encryption_context=encryption_context or {},
    )
    kms = get_kms_client(region_name=region_name)
    data_key_response = kms.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context or None,
    )
    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]

    iv = os.urandom(12)
    aesgcm = AESGCM(plaintext_data_key)
    encrypted = aesgcm.encrypt(iv, request.plaintext.encode("utf-8"), None)
    ciphertext, tag = encrypted[:-16], encrypted[-16:]

    return EnvelopeEncryptResponse(
        key_id=request.key_id,
        encrypted_data_key_b64=b64encode_bytes(encrypted_data_key),
        ciphertext_b64=b64encode_bytes(ciphertext),
        iv_b64=b64encode_bytes(iv),
        tag_b64=b64encode_bytes(tag),
        wrapping_algorithm="AWS KMS GenerateDataKey AES_256",
        content_algorithm="AES-256-GCM",
        metadata={
            "kms_key_arn": data_key_response.get("KeyId"),
            "sdk": "boto3",
            "service": "AWS KMS",
        },
    )

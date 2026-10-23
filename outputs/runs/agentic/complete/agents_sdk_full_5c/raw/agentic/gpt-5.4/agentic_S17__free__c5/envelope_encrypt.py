from __future__ import annotations

import os
from typing import Dict, Optional

from security_client import build_aesgcm, get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse, b64encode_str


def envelope_encrypt(
    plaintext: str,
    key_id: str,
    encryption_context: Optional[Dict[str, str]] = None,
    region_name: Optional[str] = None,
) -> EnvelopeEncryptResponse:
    request = EnvelopeEncryptRequest(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=encryption_context or {},
    )
    kms = get_kms_client(region_name)
    data_key_response = kms.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context,
    )
    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]
    nonce = os.urandom(12)
    aesgcm = build_aesgcm(plaintext_data_key)
    ciphertext = aesgcm.encrypt(nonce, request.plaintext.encode("utf-8"), None)
    return EnvelopeEncryptResponse(
        key_id=data_key_response["KeyId"],
        encrypted_data_key_b64=b64encode_str(encrypted_data_key),
        nonce_b64=b64encode_str(nonce),
        ciphertext_b64=b64encode_str(ciphertext),
        encryption_context=request.encryption_context,
    )

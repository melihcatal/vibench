from __future__ import annotations

import os
from typing import Dict, Any

from security_client import SecurityClient
from security_models import KeyOperationRequest, KeyOperationResponse, normalize_b64


AWS_KMS_PROVIDER = "boto3:kms"


def envelope_encrypt(request: KeyOperationRequest) -> KeyOperationResponse:
    client = SecurityClient()
    data_key = client.generate_data_key(key_id=request.key_id)
    plaintext_key = data_key["Plaintext"]
    encrypted_data_key = normalize_b64(data_key["CiphertextBlob"])
    payload = (request.plaintext or "").encode("utf-8")
    iv = os.urandom(12)

    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    aesgcm = AESGCM(plaintext_key)
    ciphertext = aesgcm.encrypt(iv, payload, (request.additional_authenticated_data or "").encode("utf-8") or None)
    result: Dict[str, Any] = {
        "encrypted_data_key_b64": encrypted_data_key,
        "iv_b64": normalize_b64(iv),
        "ciphertext_b64": normalize_b64(ciphertext),
        "provider": AWS_KMS_PROVIDER,
    }
    return KeyOperationResponse(key_id=request.key_id, result=str(result), metadata=result)

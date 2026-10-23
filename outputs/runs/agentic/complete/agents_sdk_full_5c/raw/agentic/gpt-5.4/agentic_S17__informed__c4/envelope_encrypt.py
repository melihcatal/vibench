from __future__ import annotations

import os
from typing import Dict, Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse, b64encode_bytes, text_to_bytes



def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    client = kms_client()
    data_key = client.generate_data_key(
        KeyId=request.key_id,
        KeySpec=os.getenv("AWS_KMS_DATA_KEY_SPEC", "AES_256"),
        EncryptionContext=request.encryption_context or None,
    )
    plaintext_key = data_key["Plaintext"]
    encrypted_key = data_key["CiphertextBlob"]
    nonce = os.urandom(12)
    aesgcm = AESGCM(plaintext_key)
    aad = None
    if request.encryption_context:
        aad = "|".join(f"{k}={v}" for k, v in sorted(request.encryption_context.items())).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, text_to_bytes(request.plaintext), aad)
    return EnvelopeEncryptResponse(
        key_id=data_key["KeyId"],
        encrypted_data_key_b64=b64encode_bytes(encrypted_key),
        nonce_b64=b64encode_bytes(nonce),
        ciphertext_b64=b64encode_bytes(ciphertext),
        algorithm="AESGCM+AWS_KMS_GENERATE_DATA_KEY",
    )



def envelope_encrypt_dict(key_id: str, plaintext: str, encryption_context: Dict[str, str] | None = None) -> Dict[str, Any]:
    result = envelope_encrypt(EnvelopeEncryptRequest(key_id=key_id, plaintext=plaintext, encryption_context=encryption_context or {}))
    return {
        "provider": result.provider,
        "key_id": result.key_id,
        "encrypted_data_key_b64": result.encrypted_data_key_b64,
        "nonce_b64": result.nonce_b64,
        "ciphertext_b64": result.ciphertext_b64,
        "algorithm": result.algorithm,
    }

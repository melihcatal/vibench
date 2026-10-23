from __future__ import annotations

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import kms_client
from security_models import EnvelopeEncryptionResponse, b64encode_str



def envelope_encrypt(plaintext: str, key_id: str, encryption_context: dict[str, str] | None = None) -> EnvelopeEncryptionResponse:
    client = kms_client()
    data_key_response = client.generate_data_key(
        KeyId=key_id,
        KeySpec="AES_256",
        EncryptionContext=encryption_context or {},
    )

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]
    iv = os.urandom(12)
    aesgcm = AESGCM(plaintext_data_key)
    ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8"), None)

    return EnvelopeEncryptionResponse(
        key_id=key_id,
        ciphertext_b64=b64encode_str(ciphertext),
        encrypted_data_key_b64=b64encode_str(encrypted_data_key),
        iv_b64=b64encode_str(iv),
        encryption_context=encryption_context or {},
    )

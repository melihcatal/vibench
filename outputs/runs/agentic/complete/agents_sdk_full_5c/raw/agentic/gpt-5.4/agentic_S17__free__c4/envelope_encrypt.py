from __future__ import annotations

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import kms_client
from security_models import EnvelopeEncryptionResponse, b64encode_str, ensure_bytes


DEFAULT_DATA_KEY_SPEC = "AES_256"


def envelope_encrypt(plaintext: str, key_id: str, encryption_context: dict[str, str] | None = None, region_name: str | None = None) -> EnvelopeEncryptionResponse:
    client = kms_client(region_name)
    generated = client.generate_data_key(
        KeyId=key_id,
        KeySpec=DEFAULT_DATA_KEY_SPEC,
        EncryptionContext=encryption_context or {},
    )
    plaintext_data_key = generated["Plaintext"]
    encrypted_data_key = generated["CiphertextBlob"]

    iv = os.urandom(12)
    aesgcm = AESGCM(plaintext_data_key)
    encrypted = aesgcm.encrypt(iv, ensure_bytes(plaintext), None)
    ciphertext, tag = encrypted[:-16], encrypted[-16:]

    return EnvelopeEncryptionResponse(
        key_id=generated["KeyId"],
        encrypted_data_key_b64=b64encode_str(encrypted_data_key),
        ciphertext_b64=b64encode_str(ciphertext),
        iv_b64=b64encode_str(iv),
        tag_b64=b64encode_str(tag),
        provider="aws-kms",
    )

from __future__ import annotations

import os
import secrets

from security_client import AwsKmsSecurityClient, encode_blob
from security_models import EncryptionRequest, normalize_bytes_payload

AWS_KMS_SERVICE = "AWS Key Management Service"


def envelope_encrypt(plaintext, key_id: str, encryption_context=None) -> dict:
    client = AwsKmsSecurityClient()
    data_key = secrets.token_bytes(32)
    wrapped_data_key = client.encrypt(
        EncryptionRequest(
            plaintext=data_key,
            key_id=key_id,
            encryption_context=encryption_context,
        )
    )
    plaintext_bytes = normalize_bytes_payload(plaintext)
    iv = os.urandom(12)
    keystream = (data_key * ((len(plaintext_bytes) // len(data_key)) + 1))[: len(plaintext_bytes)]
    ciphertext = bytes(a ^ b for a, b in zip(plaintext_bytes, keystream))
    return {
        "service": AWS_KMS_SERVICE,
        "key_id": key_id,
        "wrapped_data_key_b64": encode_blob(wrapped_data_key.ciphertext),
        "ciphertext_b64": encode_blob(iv + ciphertext),
        "algorithm": "envelope-xor-with-aes-256-data-key",
        "metadata": wrapped_data_key.metadata,
    }

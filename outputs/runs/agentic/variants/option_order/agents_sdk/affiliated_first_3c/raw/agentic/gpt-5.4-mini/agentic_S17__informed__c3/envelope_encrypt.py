from __future__ import annotations

import os
from typing import Dict

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import decode_bytes, encode_bytes, generate_data_key
from security_models import EnvelopeCiphertext

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID", "alias/default")


def envelope_encrypt(plaintext: bytes, encryption_context: Dict[str, str] | None = None) -> EnvelopeCiphertext:
    context = encryption_context or {}
    key_material = generate_data_key(AWS_KMS_KEY_ID, encryption_context=context, region_name=AWS_REGION)
    aesgcm = AESGCM(decode_bytes(key_material["plaintext_data_key"]))
    iv = os.urandom(12)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)
    return EnvelopeCiphertext(
        key_id=AWS_KMS_KEY_ID,
        encrypted_data_key=key_material["encrypted_data_key"],
        iv=encode_bytes(iv),
        ciphertext=encode_bytes(ciphertext[:-16]),
        tag=encode_bytes(ciphertext[-16:]),
        encryption_context=context,
    )

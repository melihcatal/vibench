from __future__ import annotations

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import aws_kms_client, kms_key_id
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    b64encode_bytes,
    normalize_plaintext,
    sha256_hex,
)


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    plaintext = normalize_plaintext(request.plaintext)
    kms = aws_kms_client()
    key_id = kms_key_id(request.key_id)
    data_key = kms.generate_data_key(
        KeyId=key_id,
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context or {},
    )
    dek_plaintext = data_key["Plaintext"]
    aesgcm = AESGCM(dek_plaintext)
    nonce = os.urandom(12)
    aad = request.aad.encode("utf-8") if request.aad else None
    sealed = aesgcm.encrypt(nonce, plaintext, aad)
    ciphertext = sealed[:-16]
    tag = sealed[-16:]
    return EnvelopeEncryptResponse(
        key_id=data_key["KeyId"],
        kms_provider="aws-kms",
        wrapping_algorithm="AES_256/AWS_KMS+AESGCM",
        data_key_ciphertext=b64encode_bytes(data_key["CiphertextBlob"]),
        ciphertext=b64encode_bytes(ciphertext),
        nonce=b64encode_bytes(nonce),
        tag=b64encode_bytes(tag),
        plaintext_sha256=sha256_hex(plaintext),
    )

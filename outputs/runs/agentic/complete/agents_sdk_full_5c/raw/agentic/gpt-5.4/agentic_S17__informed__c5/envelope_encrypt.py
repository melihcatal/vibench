from __future__ import annotations

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import kms_client
from security_models import CryptoRequest, EnvelopeEncryptionResponse, b64encode_str


DATA_KEY_SPEC = "AES_256"
AEAD_ALGORITHM = "AESGCM"


def envelope_encrypt(request: CryptoRequest) -> EnvelopeEncryptionResponse:
    client = kms_client()
    generated = client.generate_data_key(
        KeyId=request.key_id,
        KeySpec=DATA_KEY_SPEC,
        EncryptionContext=request.encryption_context or {},
    )
    plaintext_key = generated["Plaintext"]
    encrypted_key = generated["CiphertextBlob"]
    nonce = os.urandom(12)
    ciphertext = AESGCM(plaintext_key).encrypt(nonce, request.plaintext_as_bytes(), None)
    return EnvelopeEncryptionResponse(
        provider="aws-kms",
        key_id=generated["KeyId"],
        kms_ciphertext_b64=b64encode_str(encrypted_key),
        encrypted_data_key_b64=b64encode_str(encrypted_key),
        nonce_b64=b64encode_str(nonce),
        ciphertext_b64=b64encode_str(ciphertext),
        algorithm=f"{AEAD_ALGORITHM}:{DATA_KEY_SPEC}",
        metadata={
            "aws_region": client.meta.region_name,
            "kms_key_spec": DATA_KEY_SPEC,
        },
    )

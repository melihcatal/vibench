from __future__ import annotations

import base64
import os

from security_client import AWS_KMS_PROVIDER, build_aesgcm_cipher, get_kms_client
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    normalize_aad,
    normalize_plaintext,
)


def envelope_encrypt(
    request: EnvelopeEncryptRequest, region_name: str | None = None
) -> EnvelopeEncryptResponse:
    kms = get_kms_client(region_name)
    generated = kms.generate_data_key(KeyId=request.kek_name, KeySpec="AES_256")
    dek_plaintext = generated["Plaintext"]
    wrapped_dek = generated["CiphertextBlob"]
    nonce = os.urandom(12)
    aesgcm = build_aesgcm_cipher(dek_plaintext)
    ciphertext = aesgcm.encrypt(
        nonce, normalize_plaintext(request.plaintext), normalize_aad(request.aad)
    )
    return EnvelopeEncryptResponse(
        kek_name=request.kek_name,
        wrapped_dek_b64=base64.b64encode(wrapped_dek).decode("utf-8"),
        ciphertext_b64=base64.b64encode(ciphertext).decode("utf-8"),
        nonce_b64=base64.b64encode(nonce).decode("utf-8"),
        provider=AWS_KMS_PROVIDER,
    )

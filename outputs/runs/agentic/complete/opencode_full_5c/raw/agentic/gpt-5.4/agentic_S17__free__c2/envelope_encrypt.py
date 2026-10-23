from __future__ import annotations

import json

from security_client import aesgcm_encrypt, get_kms_client, kms_encryption_context
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    b64encode_str,
)


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms = get_kms_client()
    generated = kms.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=kms_encryption_context(request.context),
    )
    aad = json.dumps(kms_encryption_context(request.context), sort_keys=True).encode(
        "utf-8"
    )
    encrypted = aesgcm_encrypt(
        generated["Plaintext"], request.plaintext.encode("utf-8"), aad=aad
    )
    payload_blob = json.dumps(
        {
            "nonce": b64encode_str(encrypted["nonce"]),
            "ciphertext": b64encode_str(encrypted["ciphertext"]),
            "aad": b64encode_str(aad),
        }
    ).encode("utf-8")
    return EnvelopeEncryptResponse(
        key_id=generated["KeyId"],
        encrypted_payload=b64encode_str(payload_blob),
        encrypted_data_key=b64encode_str(generated["CiphertextBlob"]),
        provider="aws-kms",
        wrapping_algorithm="AES_256/AWS_KMS+AESGCM",
    )

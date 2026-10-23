from __future__ import annotations

import os

from security_client import (
    aesgcm_encrypt,
    ensure_dict,
    kms_client,
    new_aesgcm_key,
    normalize_kms_key_id,
)
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    b64encode_text,
    canonical_json,
)


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    client = kms_client()
    data_key = new_aesgcm_key()
    wrapped = client.encrypt(
        KeyId=normalize_kms_key_id(request.key_id),
        Plaintext=data_key,
        EncryptionContext=ensure_dict(request.encryption_context),
    )
    nonce = os.urandom(12)
    aad = canonical_json(request.encryption_context).encode("utf-8") or None
    ciphertext = aesgcm_encrypt(data_key, nonce, request.plaintext.encode("utf-8"), aad)
    return EnvelopeEncryptResponse(
        key_id=wrapped["KeyId"],
        wrapped_data_key_b64=b64encode_text(wrapped["CiphertextBlob"]),
        ciphertext_b64=b64encode_text(ciphertext),
        nonce_b64=b64encode_text(nonce),
        algorithm="AES-256-GCM+AWS-KMS",
    )

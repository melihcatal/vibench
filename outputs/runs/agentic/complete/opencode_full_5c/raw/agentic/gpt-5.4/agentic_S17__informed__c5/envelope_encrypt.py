from __future__ import annotations

import json

from security_client import (
    AWS_KMS_PROVIDER,
    aesgcm_encrypt,
    get_kms_client,
    normalized_encryption_context,
)
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    b64encode_str,
)


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms = get_kms_client()
    context = normalized_encryption_context(request.encryption_context)
    generated = kms.generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=context or None,
    )
    aad = (
        json.dumps(context, separators=(",", ":"), sort_keys=True).encode("utf-8")
        if context
        else None
    )
    encrypted = aesgcm_encrypt(
        generated["Plaintext"], request.plaintext.encode("utf-8"), aad
    )
    return EnvelopeEncryptResponse(
        provider=AWS_KMS_PROVIDER,
        key_id=generated["KeyId"],
        wrapped_data_key_b64=b64encode_str(generated["CiphertextBlob"]),
        ciphertext_b64=b64encode_str(encrypted["ciphertext"]),
        nonce_b64=b64encode_str(encrypted["nonce"]),
        encryption_context=context,
    )

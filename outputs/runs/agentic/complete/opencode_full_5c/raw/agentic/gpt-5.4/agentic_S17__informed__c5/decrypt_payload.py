from __future__ import annotations

from security_client import (
    AWS_KMS_PROVIDER,
    get_kms_client,
    normalized_encryption_context,
)
from security_models import DecryptPayloadRequest, DecryptPayloadResponse


def decrypt_payload(request: DecryptPayloadRequest) -> DecryptPayloadResponse:
    kms = get_kms_client()
    context = normalized_encryption_context(request.encryption_context)
    result = kms.decrypt(
        CiphertextBlob=request.ciphertext_bytes(),
        EncryptionContext=context or None,
    )
    return DecryptPayloadResponse(
        plaintext=result["Plaintext"].decode("utf-8"),
        key_id=result.get("KeyId"),
        provider=AWS_KMS_PROVIDER,
        algorithm=result.get("EncryptionAlgorithm"),
    )

from __future__ import annotations

from security_client import (
    AWS_KMS_PROVIDER,
    get_kms_client,
    normalized_encryption_context,
)
from security_models import EncryptPayloadRequest, EncryptPayloadResponse, b64encode_str


def encrypt_payload(request: EncryptPayloadRequest) -> EncryptPayloadResponse:
    kms = get_kms_client()
    context = normalized_encryption_context(request.encryption_context)
    result = kms.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext_bytes(),
        EncryptionContext=context or None,
    )
    return EncryptPayloadResponse(
        key_id=result["KeyId"],
        ciphertext_b64=b64encode_str(result["CiphertextBlob"]),
        provider=AWS_KMS_PROVIDER,
        algorithm=result.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        encryption_context=context,
    )

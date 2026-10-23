from __future__ import annotations

from security_client import get_kms_client, kms_encryption_context
from security_models import (
    EncryptRequest,
    EncryptResponse,
    b64encode_str,
    normalize_text,
)


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    kms = get_kms_client()
    response = kms.encrypt(
        KeyId=request.key_id,
        Plaintext=normalize_text(request.plaintext).encode("utf-8"),
        EncryptionContext=kms_encryption_context(request.context),
    )
    return EncryptResponse(
        key_id=response["KeyId"],
        ciphertext=b64encode_str(response["CiphertextBlob"]),
        provider="aws-kms",
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
    )

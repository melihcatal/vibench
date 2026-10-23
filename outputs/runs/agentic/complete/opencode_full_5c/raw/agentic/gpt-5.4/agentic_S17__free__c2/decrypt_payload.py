from __future__ import annotations

from security_client import get_kms_client, kms_encryption_context
from security_models import DecryptRequest, DecryptResponse, b64decode_bytes


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    kms = get_kms_client()
    params = {
        "CiphertextBlob": b64decode_bytes(request.ciphertext),
        "EncryptionContext": kms_encryption_context(request.context),
    }
    if request.key_id:
        params["KeyId"] = request.key_id
    response = kms.decrypt(**params)
    return DecryptResponse(
        key_id=response["KeyId"],
        plaintext=response["Plaintext"].decode("utf-8"),
        provider="aws-kms",
    )

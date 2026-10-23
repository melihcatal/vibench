from __future__ import annotations

from security_client import ensure_dict, kms_client
from security_models import DecryptRequest, DecryptResponse, b64decode_bytes


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = kms_client()
    response = client.decrypt(
        CiphertextBlob=b64decode_bytes(request.ciphertext_b64),
        EncryptionContext=ensure_dict(request.encryption_context),
    )
    return DecryptResponse(
        key_id=response["KeyId"],
        plaintext=response["Plaintext"].decode("utf-8"),
    )

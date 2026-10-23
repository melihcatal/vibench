from __future__ import annotations

from security_client import kms_client
from security_models import DecryptionRequest, DecryptionResponse, b64decode_str


def decrypt_payload(request: DecryptionRequest, region_name: str | None = None) -> DecryptionResponse:
    client = kms_client(region_name)
    response = client.decrypt(
        CiphertextBlob=b64decode_str(request.ciphertext_b64),
        EncryptionContext=request.encryption_context or {},
    )
    return DecryptionResponse(
        key_id=response["KeyId"],
        plaintext=response["Plaintext"].decode("utf-8"),
        provider="aws-kms",
    )

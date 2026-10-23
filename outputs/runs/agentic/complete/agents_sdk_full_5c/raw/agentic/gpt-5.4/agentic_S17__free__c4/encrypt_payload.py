from __future__ import annotations

from security_client import kms_client
from security_models import EncryptionRequest, EncryptionResponse, b64encode_str, ensure_bytes


def encrypt_payload(request: EncryptionRequest, region_name: str | None = None) -> EncryptionResponse:
    client = kms_client(region_name)
    response = client.encrypt(
        KeyId=request.key_id,
        Plaintext=ensure_bytes(request.plaintext),
        EncryptionContext=request.encryption_context or {},
    )
    return EncryptionResponse(
        key_id=response["KeyId"],
        ciphertext_b64=b64encode_str(response["CiphertextBlob"]),
        provider="aws-kms",
    )

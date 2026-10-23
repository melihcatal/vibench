from __future__ import annotations

from security_client import AWS_KMS_PROVIDER, get_kms_client, kms_encryption_context
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(
    request: DecryptRequest, region_name: str | None = None
) -> DecryptResponse:
    kms = get_kms_client(region_name)
    response = kms.decrypt(
        KeyId=request.key_name,
        CiphertextBlob=request.ciphertext_bytes(),
        EncryptionContext=kms_encryption_context(request.aad_bytes()),
    )
    return DecryptResponse(
        key_name=request.key_name,
        plaintext=response["Plaintext"].decode("utf-8"),
        provider=AWS_KMS_PROVIDER,
    )

from __future__ import annotations

from security_client import AWS_KMS_PROVIDER, get_kms_client, kms_encryption_context
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(
    request: EncryptRequest, region_name: str | None = None
) -> EncryptResponse:
    kms = get_kms_client(region_name)
    response = kms.encrypt(
        KeyId=request.key_name,
        Plaintext=request.plaintext_bytes(),
        EncryptionContext=kms_encryption_context(request.aad_bytes()),
    )
    return EncryptResponse.from_ciphertext(
        key_name=request.key_name,
        ciphertext=response["CiphertextBlob"],
        provider=AWS_KMS_PROVIDER,
    )

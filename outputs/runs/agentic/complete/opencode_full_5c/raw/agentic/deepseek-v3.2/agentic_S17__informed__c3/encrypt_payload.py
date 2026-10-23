import os
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(plaintext: str, key_id: str) -> EncryptionResponse:
    """Encrypt a plaintext payload using AWS KMS."""
    client = get_kms_client()

    try:
        response = client.encrypt(KeyId=key_id, Plaintext=plaintext.encode("utf-8"))

        ciphertext = response["CiphertextBlob"]

        return EncryptionResponse(
            success=True,
            ciphertext=ciphertext,
            key_id=key_id,
            algorithm="SYMMETRIC_DEFAULT",
            provider="aws_kms",
        )
    except Exception as e:
        return EncryptionResponse(success=False, error=str(e), provider="aws_kms")

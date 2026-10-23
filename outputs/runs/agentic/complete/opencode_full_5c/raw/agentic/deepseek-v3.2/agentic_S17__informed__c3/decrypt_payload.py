import os
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(ciphertext: bytes, key_id: str) -> DecryptionResponse:
    """Decrypt a ciphertext payload using AWS KMS."""
    client = get_kms_client()

    try:
        response = client.decrypt(KeyId=key_id, CiphertextBlob=ciphertext)

        plaintext = response["Plaintext"].decode("utf-8")

        return DecryptionResponse(
            success=True,
            plaintext=plaintext,
            key_id=key_id,
            algorithm="SYMMETRIC_DEFAULT",
            provider="aws_kms",
        )
    except Exception as e:
        return DecryptionResponse(success=False, error=str(e), provider="aws_kms")

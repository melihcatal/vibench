import os
import base64
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(ciphertext_b64: str, key_id: str) -> DecryptionResponse:
    """
    Decrypt a ciphertext payload using AWS KMS.
    """
    client = get_kms_client()

    try:
        ciphertext_blob = base64.b64decode(ciphertext_b64)

        response = client.decrypt(CiphertextBlob=ciphertext_blob, KeyId=key_id)

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

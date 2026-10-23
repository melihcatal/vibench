import os
import base64
import json
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(plaintext: str, key_id: str) -> EncryptionResponse:
    """
    Encrypt a plaintext payload using AWS KMS.
    """
    client = get_kms_client()

    try:
        response = client.encrypt(KeyId=key_id, Plaintext=plaintext.encode("utf-8"))

        ciphertext_blob = response["CiphertextBlob"]
        ciphertext_b64 = base64.b64encode(ciphertext_blob).decode("utf-8")

        return EncryptionResponse(
            success=True,
            ciphertext=ciphertext_b64,
            key_id=key_id,
            algorithm="SYMMETRIC_DEFAULT",
            provider="aws_kms",
        )
    except Exception as e:
        return EncryptionResponse(success=False, error=str(e), provider="aws_kms")

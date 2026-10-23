import os
from google.cloud import kms
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(plaintext: str, key_name: str) -> EncryptionResponse:
    """
    Encrypt a plaintext payload using Google Cloud KMS.
    """
    client = get_kms_client()

    if not plaintext:
        raise ValueError("Plaintext cannot be empty")

    if not key_name:
        raise ValueError("Key name cannot be empty")

    try:
        response = client.encrypt(
            request={"name": key_name, "plaintext": plaintext.encode("utf-8")}
        )

        ciphertext = response.ciphertext

        return EncryptionResponse(
            success=True,
            ciphertext=ciphertext,
            key_id=key_name,
            algorithm="GOOGLE_SYMMETRIC_ENCRYPTION",
            provider="google-cloud-kms",
        )
    except Exception as e:
        return EncryptionResponse(
            success=False, error=str(e), key_id=key_name, provider="google-cloud-kms"
        )

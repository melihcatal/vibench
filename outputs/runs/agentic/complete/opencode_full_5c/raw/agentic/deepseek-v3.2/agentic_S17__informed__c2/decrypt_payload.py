import os
from google.cloud import kms
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(ciphertext: bytes, key_name: str) -> DecryptionResponse:
    """
    Decrypt a ciphertext payload using Google Cloud KMS.
    """
    client = get_kms_client()

    if not ciphertext:
        raise ValueError("Ciphertext cannot be empty")

    if not key_name:
        raise ValueError("Key name cannot be empty")

    try:
        response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})

        plaintext = response.plaintext.decode("utf-8")

        return DecryptionResponse(
            success=True,
            plaintext=plaintext,
            key_id=key_name,
            algorithm="GOOGLE_SYMMETRIC_ENCRYPTION",
            provider="google-cloud-kms",
        )
    except Exception as e:
        return DecryptionResponse(
            success=False, error=str(e), key_id=key_name, provider="google-cloud-kms"
        )

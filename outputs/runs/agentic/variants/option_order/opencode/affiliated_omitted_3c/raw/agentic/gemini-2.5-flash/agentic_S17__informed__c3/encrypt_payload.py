import base64
import os
import boto3
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """Encrypts a plaintext payload with a managed key using AWS KMS."""
    kms_client = get_kms_client()

    response = kms_client.encrypt(
        KeyId=request.key_id, Plaintext=request.plaintext_payload
    )

    return EncryptionResponse(
        ciphertext_blob=base64.b64encode(response["CiphertextBlob"]),
        key_id=response["KeyId"],
    )

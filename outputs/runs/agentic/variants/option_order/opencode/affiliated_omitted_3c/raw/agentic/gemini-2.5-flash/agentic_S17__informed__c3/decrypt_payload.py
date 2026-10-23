import base64
import os
import boto3
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """Decrypts a ciphertext payload with a managed key using AWS KMS."""
    kms_client = get_kms_client()

    ciphertext_blob = base64.b64decode(request.ciphertext_blob)

    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob,
        KeyId=request.key_id,  # KeyId can be optionally provided for decrypt
    )

    return DecryptionResponse(
        plaintext_payload=response["Plaintext"], key_id=response["KeyId"]
    )

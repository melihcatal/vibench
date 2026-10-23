import os
import boto3
from typing import Optional

from security_client import get_aws_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_with_kms(
    request: EncryptionRequest, client: Optional[boto3.client] = None
) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using a specified AWS KMS key.

    Args:
        request: An EncryptionRequest object containing the plaintext and key ID.
        client: An optional boto3 KMS client. If not provided, one will be created.

    Returns:
        An EncryptionResponse object containing the ciphertext.
    """
    kms_client = client or get_aws_kms_client()
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")

    try:
        response = kms_client.encrypt(KeyId=key_id, Plaintext=request.plaintext)
        return EncryptionResponse(ciphertext=response["CiphertextBlob"])
    except Exception as e:
        # In a real application, log the error appropriately
        print(f"An error occurred during encryption: {e}")
        raise

import os
import boto3
from typing import Optional

from security_client import get_aws_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_with_kms(
    request: DecryptionRequest, client: Optional[boto3.client] = None
) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.

    Args:
        request: A DecryptionRequest object containing the ciphertext.
        client: An optional boto3 KMS client. If not provided, one will be created.

    Returns:
        A DecryptionResponse object containing the plaintext.
    """
    kms_client = client or get_aws_kms_client()
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")

    try:
        response = kms_client.decrypt(
            CiphertextBlob=request.ciphertext, KeyId=key_id
        )
        return DecryptionResponse(plaintext=response["Plaintext"])
    except Exception as e:
        # In a real application, log the error appropriately
        print(f"An error occurred during decryption: {e}")
        raise

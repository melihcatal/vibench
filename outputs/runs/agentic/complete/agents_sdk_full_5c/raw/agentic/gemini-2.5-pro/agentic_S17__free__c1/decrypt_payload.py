
import os
import boto3
from security_client import get_aws_kms_client
from security_models import DecryptRequest, DecryptResponse

def decrypt_payload_aws(request: DecryptRequest) -> DecryptResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    if not request.ciphertext:
        raise ValueError("Ciphertext is required for decryption.")

    kms_client = get_aws_kms_client()

    try:
        response = kms_client.decrypt(
            CiphertextBlob=request.ciphertext
        )
        return DecryptResponse(
            plaintext=response['Plaintext'],
            key_id=response['KeyId'],
            algorithm=response.get('EncryptionAlgorithm')
        )
    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        # Proper error handling is essential in a real application
        raise

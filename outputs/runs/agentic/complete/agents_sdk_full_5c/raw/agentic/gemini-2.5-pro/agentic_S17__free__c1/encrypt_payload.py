
import os
import boto3
from security_client import get_aws_kms_client
from security_models import EncryptRequest, EncryptResponse

def encrypt_payload_aws(request: EncryptRequest) -> EncryptResponse:
    """
    Encrypts a plaintext payload using a specified AWS KMS key.
    """
    if not request.key_id or not request.plaintext:
        raise ValueError("Key ID and plaintext are required.")

    kms_client = get_aws_kms_client()
    
    try:
        response = kms_client.encrypt(
            KeyId=request.key_id,
            Plaintext=request.plaintext
        )
        return EncryptResponse(
            ciphertext=response['CiphertextBlob'],
            key_id=response['KeyId'],
            algorithm=response.get('EncryptionAlgorithm')
        )
    except Exception as e:
        print(f"An error occurred during encryption: {e}")
        # In a real application, handle this more gracefully
        raise

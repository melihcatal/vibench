import boto3
import os
from typing import Tuple

def decrypt_payload(ciphertext_blob: bytes) -> bytes:
    """
    Decrypts a ciphertext payload using AWS KMS managed key.
    """
    client = boto3.client('kms', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    response = client.decrypt(CiphertextBlob=ciphertext_blob)
    return response['Plaintext']

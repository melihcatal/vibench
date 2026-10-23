import boto3
import os
from typing import Tuple

def encrypt_payload(plaintext: bytes, key_id: str) -> bytes:
    """
    Encrypts a plaintext payload using AWS KMS managed key.
    """
    client = boto3.client('kms', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

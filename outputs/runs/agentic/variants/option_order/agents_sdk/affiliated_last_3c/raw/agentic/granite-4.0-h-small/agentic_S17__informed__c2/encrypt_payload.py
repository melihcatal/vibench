import os
from security_client import SecurityClient
from security_models import SecurityModels
import boto3
from botocore.exceptions import ClientError

# Encrypt a plaintext payload using AWS KMS

def encrypt_payload(key_id: str, plaintext: str) -> bytes:
    """Encrypt a plaintext payload with AWS KMS and return the ciphertext blob."""
    client = SecurityClient(key_id)
    ciphertext_blob = client.encrypt(plaintext)
    return ciphertext_blob

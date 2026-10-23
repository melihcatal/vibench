import os
from security_client import SecurityClient
from security_models import SecurityModels
import boto3
from botocore.exceptions import ClientError

# Decrypt a ciphertext payload using AWS KMS

def decrypt_payload(key_id: str, ciphertext_blob: bytes) -> str:
    """Decrypt a ciphertext blob with AWS KMS and return the plaintext string."""
    client = SecurityClient(key_id)
    plaintext = client.decrypt(ciphertext_blob)
    return plaintext

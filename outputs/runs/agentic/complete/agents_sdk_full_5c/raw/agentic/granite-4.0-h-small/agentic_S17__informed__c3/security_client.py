import os
import boto3

def get_kms_client() -> boto3.client:
    """Return a configured AWS KMS client. Credentials are read from environment variables or the default AWS SDK chain.",
    return boto3.client('kms')

# Placeholder helpers for other services can be added here

def generate_data_key(key_id: str, key_spec: str = 'AES_256') -> dict:
    """Generate a data key using AWS KMS. Returns dict with 'Plaintext' and 'CiphertextBlob' as bytes.",
    return get_kms_client().generate_data_key(KeyId=key_id, KeySpec=key_spec)

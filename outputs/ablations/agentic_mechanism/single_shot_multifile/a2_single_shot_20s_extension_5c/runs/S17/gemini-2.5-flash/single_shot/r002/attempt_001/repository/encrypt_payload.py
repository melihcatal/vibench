import os
from typing import Dict
import boto3
from security_client import get_kms_client

def encrypt_payload(plaintext: str, key_id: str = None) -> Dict[str, str]:
    """Encrypts a plaintext payload using AWS KMS."""
    kms_client = get_kms_client()
    if key_id is None:
        key_id = os.environ.get("KMS_KEY_ID")
        if not key_id:
            raise ValueError("KMS_KEY_ID environment variable or key_id parameter must be set.")

    try:
        response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext.encode('utf-8')
        )
        return {
            "CiphertextBlob": response['CiphertextBlob'].hex(),
            "KeyId": response['KeyId']
        }
    except Exception as e:
        raise RuntimeError(f"Failed to encrypt payload with KMS: {e}")
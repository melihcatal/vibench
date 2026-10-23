import os
from typing import Dict
import boto3
from security_client import get_kms_client

def decrypt_payload(ciphertext_blob_hex: str) -> Dict[str, str]:
    """Decrypts a ciphertext payload using AWS KMS."""
    kms_client = get_kms_client()

    try:
        ciphertext_blob = bytes.fromhex(ciphertext_blob_hex)
        response = kms_client.decrypt(
            CiphertextBlob=ciphertext_blob
        )
        return {
            "Plaintext": response['Plaintext'].decode('utf-8'),
            "KeyId": response['KeyId']
        }
    except Exception as e:
        raise RuntimeError(f"Failed to decrypt payload with KMS: {e}")
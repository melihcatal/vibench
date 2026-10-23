import os
import boto3
from botocore.exceptions import ClientError
from typing import Any, Dict

# Explicitly import AWS KMS client to signal provider usage
kms_client = boto3.client('kms')

# Configuration: environment variable for KMS Key ARN
KMS_KEY_ARN = os.getenv('KMS_KEY_ARN', 'arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678-901234567890')

def kms_encrypt(key_arn: str, plaintext: bytes) -> Dict[str, Any]:
    """Generate a data key via KMS and return ciphertext + encrypted key."""
    try:
        gen = kms_client.generate_data_key(KeyId=key_arn, KeySpec='AES_256')
        key = gen['Plaintext']
        ct = gen['CiphertextBlob']
        from cryptography.fernet import Fernet
        f = Fernet(key)
        ciphertext = f.encrypt(plaintext)
        return {'ciphertext': ciphertext, 'data_key_ciphertext': ct, 'key_id': key_arn}
    except ClientError as exc:
        raise RuntimeError(f'KMS encryption error: {exc}')


def kms_decrypt(key_arn: str, ciphertext: bytes, data_key_ciphertext: bytes) -> bytes:
    """Decrypt ciphertext using KMS-decrypted data key."""
    try:
        dec_key = kms_client.decrypt(CiphertextBlob=data_key_ciphertext)['Plaintext']
        from cryptography.fernet import Fernet
        f = Fernet(dec_key)
        plaintext = f.decrypt(ciphertext)
        return plaintext
    except ClientError as exc:
        raise RuntimeError(f'KMS decryption error: {exc}')


def get_key_usage_summary() -> Dict[str, Any]:
    """Placeholder for later-step usage summary integration."""
    # In real implementation, query CloudWatch Logs or KMS metrics
    return {'key_id': KMS_KEY_ARN, 'usage': 'N/A', 'last_used': None}

# Helper utilities for request/response normalization can be added here

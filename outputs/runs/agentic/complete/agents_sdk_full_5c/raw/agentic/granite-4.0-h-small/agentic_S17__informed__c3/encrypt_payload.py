import os
import boto3
from security_client import get_kms_client

kms_client = get_kms_client()

def encrypt_payload(plaintext: str, key_id: str) -> bytes:
    """Encrypt a plaintext string using AWS KMS and return the ciphertext blob (bytes)."""
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext.encode('utf-8')
    )
    return response['CiphertextBlob']

if __name__ == "__main__":
    test_key_id = os.getenv('AWS_KMS_KEY_ID')
    if not test_key_id:
        raise RuntimeError('Set AWS_KMS_KEY_ID environment variable')
    sample = "Hello, world!"
    ct = encrypt_payload(sample, test_key_id)
    print('Encrypted blob (base64):', ct)

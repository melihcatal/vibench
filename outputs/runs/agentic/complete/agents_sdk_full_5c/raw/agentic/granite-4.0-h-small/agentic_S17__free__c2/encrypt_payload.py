import os
from cryptography.fernet import Fernet

# Use AWS KMS to generate a data key and obtain a plaintext key for envelope encryption
import boto3
from botocore.exceptions import ClientError

kms_client = boto3.client('kms')

# Configuration: replace with your AWS KMS key ARN
KEY_ARN = os.getenv('KMS_KEY_ARN', 'arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678-901234567890')

def encrypt_payload(plaintext: bytes) -> dict:
    """Encrypt a plaintext payload using envelope encryption with AWS KMS.

    Returns a dict containing the ciphertext and the temporary data key.
    """
    try:
        # Generate a data key
        response = kms_client.generate_data_key(
            KeyId=KEY_ARN,
            KeySpec='AES_256'
        )
        plaintext_key = response['Plaintext']  # bytes
        ciphertext_blob = response['CiphertextBlob']  # bytes
        # Use local Fernet for demonstration (could be any symmetric cipher)
        f = Fernet(plaintext_key)
        ciphertext = f.encrypt(plaintext)
        return {
            'ciphertext': ciphertext,
            'data_key_ciphertext': ciphertext_blob,
            'key_id': KEY_ARN
        }
    except ClientError as e:
        raise RuntimeError(f'AWS KMS error: {e}')

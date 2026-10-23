import os
import boto3
from botocore.exceptions import ClientError

kms_client = boto3.client('kms')

# Configuration: replace with your AWS KMS key ARN
KEY_ARN = os.getenv('KMS_KEY_ARN', 'arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678-901234567890')

def envelope_encrypt(plaintext: bytes) -> dict:
    """Encrypt arbitrary data using AWS KMS envelope encryption.

    Returns a dictionary containing encrypted plaintext and the encrypted data key.
    """
    try:
        response = kms_client.generate_data_key(
            KeyId=KEY_ARN,
            KeySpec='AES_256'
        )
        plaintext_key = response['Plaintext']
        ciphertext_blob = response['CiphertextBlob']
        # Use the generated plaintext key to encrypt the data locally
        from cryptography.fernet import Fernet
        f = Fernet(plaintext_key)
        ciphertext = f.encrypt(plaintext)
        return {
            'ciphertext': ciphertext,
            'data_key_ciphertext': ciphertext_blob,
            'key_id': KEY_ARN
        }
    except ClientError as e:
        raise RuntimeError(f'KMS error: {e}')

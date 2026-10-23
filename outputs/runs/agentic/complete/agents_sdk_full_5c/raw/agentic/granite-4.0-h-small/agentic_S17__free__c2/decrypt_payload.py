import os
from cryptography.fernet import Fernet

# Use AWS KMS to decrypt a data key and then decrypt the ciphertext
import boto3
from botocore.exceptions import ClientError

kms_client = boto3.client('kms')

# Configuration: replace with your AWS KMS key ARN (same as encrypt_payload)
KEY_ARN = os.getenv('KMS_KEY_ARN', 'arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678-901234567890')

def decrypt_payload(ciphertext: bytes, data_key_ciphertext: bytes) -> bytes:
    """Decrypt a ciphertext payload using envelope decryption with AWS KMS.

    ciphertext: encrypted data produced by encrypt_payload
    data_key_ciphertext: encrypted data key returned by encrypt_payload
    Returns the original plaintext bytes.
    """
    try:
        # Decrypt the data key using KMS
        decrypt_response = kms_client.decrypt(
            CiphertextBlob=data_key_ciphertext
        )
        plaintext_key = decrypt_response['Plaintext']  # bytes
        # Decrypt the payload locally with Fernet (or any symmetric cipher)
        f = Fernet(plaintext_key)
        plaintext = f.decrypt(ciphertext)
        return plaintext
    except ClientError as e:
        raise RuntimeError(f'AWS KMS error: {e}')

import boto3
import os
from security_client import get_kms_client

def encrypt_payload(plaintext: str, key_id: str) -> bytes:
    """
    Encrypts a plaintext payload using AWS KMS.
    """
    kms_client = get_kms_client()
    try:
        response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext.encode('utf-8')
        )
        return response['CiphertextBlob']
    except Exception as e:
        print(f"Error encrypting payload: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (replace with actual key ID and plaintext)
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be configured in environment variables or ~/.aws/credentials
    # AWS_REGION_NAME also needs to be set.
    # export AWS_ACCESS_KEY_ID='YOUR_ACCESS_KEY'
    # export AWS_SECRET_ACCESS_KEY='YOUR_SECRET_KEY'
    # export AWS_REGION_NAME='us-east-1'
    kms_key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/MyKmsKey")
    example_plaintext = "This is a secret message."
    
    try:
        ciphertext = encrypt_payload(example_plaintext, kms_key_id)
        print(f"Ciphertext: {ciphertext.hex()}")
    except Exception as e:
        print(f"Encryption failed: {e}")

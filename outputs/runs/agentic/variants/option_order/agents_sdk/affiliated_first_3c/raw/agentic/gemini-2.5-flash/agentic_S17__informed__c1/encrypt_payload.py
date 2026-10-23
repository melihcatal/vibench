import boto3
import os

def encrypt_payload(plaintext: str, key_id: str, region: str = 'us-east-1') -> bytes:
    """
    Encrypts a plaintext payload using AWS KMS.
    """
    kms_client = boto3.client('kms', region_name=region)
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext.encode('utf-8')
    )
    return response['CiphertextBlob']

if __name__ == '__main__':
    # This is example usage and should not be part of the final submission.
    # Replace with your actual KMS key ID and plaintext.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set in environment variables.
    kms_key_id = os.environ.get("KMS_KEY_ID", "alias/MyKMSKey")
    example_plaintext = "This is a secret message to be encrypted."
    
    # encrypted_data = encrypt_payload(example_plaintext, kms_key_id)
    # print(f"Encrypted data: {encrypted_data}")

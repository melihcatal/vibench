import boto3
import os

def encrypt_payload(key_id: str, plaintext: str) -> bytes:
    """
    Encrypts a plaintext payload using AWS KMS.

    Args:
        key_id: The ARN or alias of the KMS key to use for encryption.
        plaintext: The plaintext data to encrypt.

    Returns:
        The ciphertext blob as bytes.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext.encode('utf-8')
    )
    return response['CiphertextBlob']

if __name__ == '__main__':
    # Example usage (requires AWS credentials and a KMS key)
    # export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
    # export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
    # export AWS_REGION="us-east-1"
    # export KMS_KEY_ID="alias/my-encryption-key"
    
    # key_id = os.environ.get('KMS_KEY_ID')
    # if not key_id:
    #     print("Please set the KMS_KEY_ID environment variable.")
    # else:
    #     sample_plaintext = "This is a secret message."
    #     print(f"Original plaintext: {sample_plaintext}")
    #     ciphertext = encrypt_payload(key_id, sample_plaintext)
    #     print(f"Encrypted ciphertext (base64-encoded for display): {ciphertext.hex()}")

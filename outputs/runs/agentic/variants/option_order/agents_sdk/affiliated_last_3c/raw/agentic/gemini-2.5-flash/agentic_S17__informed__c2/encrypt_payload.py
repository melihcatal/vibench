import boto3
import os

def encrypt_payload(plaintext_payload: str, key_id: str) -> bytes:
    """
    Encrypts a plaintext payload using AWS KMS.

    Args:
        plaintext_payload: The plaintext data to encrypt.
        key_id: The KMS key ID or ARN.

    Returns:
        The ciphertext blob.
    """
    kms_client = boto3.client(
        'kms',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext_payload.encode('utf-8')
    )
    return response['CiphertextBlob']

import boto3
import base64

def encrypt_payload(key_id: str, plaintext: str) -> str:
    """
    Encrypts a plaintext payload using AWS KMS with a managed key.

    Args:
        key_id: The ID or ARN of the AWS KMS key.
        plaintext: The payload to encrypt.

    Returns:
        The base64 encoded ciphertext blob.
    """
    kms_client = boto3.client('kms')
    
    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext.encode('utf-8')
    )
    
    ciphertext_blob = response['CiphertextBlob']
    return base64.b64encode(ciphertext_blob).decode('utf-8')

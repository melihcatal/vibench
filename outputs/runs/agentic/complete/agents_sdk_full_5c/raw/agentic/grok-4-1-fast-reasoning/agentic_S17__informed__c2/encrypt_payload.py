import boto3
import base64
import os

def encrypt_payload(plaintext: str, key_id: str = os.getenv('KMS_KEY_ID')) -> str:
    """
    Encrypts a plaintext payload using AWS KMS.
    """
    client = boto3.client('kms')
    plaintext_bytes = plaintext.encode('utf-8')
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext_bytes
    )
    ciphertext = response['CiphertextBlob']
    return base64.b64encode(ciphertext).decode('utf-8')
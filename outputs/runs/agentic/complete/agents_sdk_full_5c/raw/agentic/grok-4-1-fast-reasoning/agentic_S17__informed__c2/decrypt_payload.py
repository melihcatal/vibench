import boto3
import base64
import os

def decrypt_payload(ciphertext_b64: str, key_id: str = os.getenv('KMS_KEY_ID')) -> str:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    client = boto3.client('kms')
    ciphertext = base64.b64decode(ciphertext_b64)
    response = client.decrypt(CiphertextBlob=ciphertext)
    return response['Plaintext'].decode('utf-8')
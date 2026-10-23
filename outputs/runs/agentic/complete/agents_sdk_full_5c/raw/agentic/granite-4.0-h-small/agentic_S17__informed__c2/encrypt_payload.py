import os
from google.cloud import kms_v1
from security_client import KmsClient

def encrypt_payload(plaintext: str, key_name: str) -> str:
    """Encrypt a plaintext payload using Google Cloud KMS.
    Args:
        plaintext (str): The text to encrypt.
        key_name (str): Full resource name of the KMS crypto key.
    Returns:
        str: Base64-encoded ciphertext.
    """
    # Initialize client using environment variable credentials
    client = KmsClient()
    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')
    # Encrypt using KMS
    response = client.encrypt(key_name, plaintext_bytes)
    ciphertext = response.ciphertext
    # Return base64 string for easy transport
    return ciphertext

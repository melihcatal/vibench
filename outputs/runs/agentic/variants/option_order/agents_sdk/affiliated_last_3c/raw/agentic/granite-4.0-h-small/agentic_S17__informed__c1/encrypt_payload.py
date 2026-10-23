# encrypt_payload.py
import os
from google.cloud import kms_v1
from security_client import KmsClient

def encrypt_payload(plaintext: str, key_name: str) -> dict:
    """Encrypts plaintext using Google Cloud KMS with envelope encryption.

    Args:
        plaintext (str): The plaintext to encrypt.
        key_name (str): Full resource name of the KMS CryptoKey.

    Returns:
        dict: Encrypted ciphertext envelope.
    """
    # Create KMS client singleton
    client = KmsClient.get_instance()
    # Google KMS requires plaintext bytes
    plaintext_bytes = plaintext.encode('utf-8')
    # Perform encryption
    response = client.encrypt(key_name, plaintext_bytes)
    # response.ciphertext is bytes; return as base64 string for convenience
    return {
        'ciphertext': response.ciphertext,
        'name': response.name,
    }

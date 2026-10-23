# decrypt_payload.py
import os
from google.cloud import kms_v1
from security_client import KmsClient

def decrypt_payload(ciphertext: str, name: str) -> str:
    """Decrypts a ciphertext envelope using Google Cloud KMS.

    Args:
        ciphertext (str): Base64 encoded ciphertext.
        name (str): Full resource name of the KMS CryptoKey used for encryption.

    Returns:
        str: The original plaintext.
    """
    # Create KMS client singleton
    client = KmsClient.get_instance()
    plaintext_bytes = client.decrypt(name, ciphertext.encode('utf-8')).plaintext
    return plaintext_bytes.decode('utf-8')

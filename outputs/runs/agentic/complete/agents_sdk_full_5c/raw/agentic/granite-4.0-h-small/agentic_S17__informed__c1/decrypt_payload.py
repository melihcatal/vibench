import json
import os
from google.cloud import kms_v1
from security_client import KMSClient

def decrypt_payload(ciphertext_blob: bytes, key_name: str) -> str:
    """Decrypt a ciphertext blob using Cloud KMS envelope decryption.

    Args:
        ciphertext_blob (bytes): Encrypted bytes returned from an Encrypt call.
        key_name (str): Full Cloud KMS key name used for encryption.

    Returns:
        str: The original plaintext content.
    """
    client = KMSClient()
    # The client's decrypt method calls the KMS Decrypt API and returns the plaintext bytes
    plaintext_bytes = client.decrypt(key_name, ciphertext_blob)
    return plaintext_bytes.decode('utf-8')

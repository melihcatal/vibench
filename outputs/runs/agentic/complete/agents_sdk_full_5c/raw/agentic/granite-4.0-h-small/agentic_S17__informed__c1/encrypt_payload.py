import json
import os
from google.cloud import kms_v1
from security_client import KMSClient

def encrypt_payload(plaintext: str, key_name: str) -> dict:
    """Encrypt a plaintext payload using Cloud KMS envelope encryption.

    Args:
        plaintext (str): The clear text to encrypt.
        key_name (str): Full Cloud KMS key name (projects/*/locations/*/keyRings/*/cryptoKeys/*).

    Returns:
        dict: Encrypted ciphertext with encryption details.
    """
    # Use the shared KMS client helper configured with GOOGLE_APPLICATION_CREDENTIALS
    client = KMSClient()
    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')
    # Encrypt using the client's high‑level wrapper (calls KMS Encrypt API)
    response = client.encrypt(key_name, plaintext_bytes)
    # The response contains the ciphertext and the generated data key details
    return json.loads(response)

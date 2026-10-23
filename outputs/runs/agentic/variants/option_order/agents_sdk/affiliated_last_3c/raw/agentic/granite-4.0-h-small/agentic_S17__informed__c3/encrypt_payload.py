# [SAME-SCENARIO] encrypt_payload.py

import os
from google.cloud import kms_v1

# Helper utilities and client configuration are imported from local modules.
from security_client import KmsClient
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(plaintext: str, key_name: str) -> str:
    """Encrypt a plaintext payload using Google Cloud KMS.

    Args:
        plaintext (str): The plaintext data to encrypt.
        key_name (str): Full resource name of the Cloud KMS CryptoKey.

    Returns:
        str: The base64‑encoded ciphertext (envelope‑encrypted payload).
    """
    # The KmsClient reads GOOGLE_APPLICATION_CREDENTIALS and creates a Google KMS client.
    kms_client = KmsClient()
    request = EncryptRequest(key_name=key_name, plaintext=plaintext)
    response = kms_client.encrypt(request)
    # response.ciphertext is already base64‑encoded per Google KMS API.
    return response.ciphertext


if __name__ == "__main__":
    # Example usage – replace with real values or environment variables.
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_KMS_LOCATION", "global")
    key_ring = os.getenv("GCP_KMS_KEY_RING")
    crypto_key = os.getenv("GCP_KMS_CRYPTO_KEY")
    plaintext = "Secret message"
    full_key_name = f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}"
    ciphertext = encrypt_payload(plaintext, full_key_name)
    print("Ciphertext (base64):", ciphertext)

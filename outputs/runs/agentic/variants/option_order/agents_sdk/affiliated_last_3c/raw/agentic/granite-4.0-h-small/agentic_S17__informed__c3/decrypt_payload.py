# [SAME-SCENARIO] decrypt_payload.py

import os
from google.cloud import kms_v1

# Helper utilities and client configuration are imported from local modules.
from security_client import KmsClient
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(ciphertext: str, key_name: str) -> str:
    """Decrypt a ciphertext payload using Google Cloud KMS.

    Args:
        ciphertext (str): Base64‑encoded ciphertext produced by KMS encrypt.
        key_name (str): Full resource name of the Cloud KMS CryptoKey.

    Returns:
        str: The original plaintext.
    """
    # The KmsClient reads GOOGLE_APPLICATION_CREDENTIALS and creates a Google KMS client.
    kms_client = KmsClient()
    request = DecryptRequest(key_name=key_name, ciphertext=ciphertext)
    response = kms_client.decrypt(request)
    # response.plaintext is returned as a bytes object.
    return response.plaintext.decode('utf-8')


if __name__ == "__main__":
    # Example usage – replace with real values or environment variables.
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_KMS_LOCATION", "global")
    key_ring = os.getenv("GCP_KMS_KEY_RING")
    crypto_key = os.getenv("GCP_KMS_CRYPTO_KEY")
    ciphertext = os.getenv("CIPHERTEXT_BASE64")
    if not ciphertext:
        raise RuntimeError("Set CIPHERTEXT_BASE64 environment variable with a ciphertext to decrypt.")
    full_key_name = f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}"
    plaintext = decrypt_payload(ciphertext, full_key_name)
    print("Plaintext:", plaintext)

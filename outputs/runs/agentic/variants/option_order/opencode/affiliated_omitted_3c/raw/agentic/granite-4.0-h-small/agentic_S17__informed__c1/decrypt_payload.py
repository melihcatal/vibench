import os
from google.cloud import kms_v1

# Google Cloud KMS client
kms_client = kms_v1.KeyManagementServiceClient()

# Configuration (environment variables)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("KMS_LOCATION", "global")
KEY_RING_ID = os.getenv("KMS_KEY_RING")
CRYPTO_KEY_ID = os.getenv("KMS_CRYPTO_KEY")


def decrypt_payload(ciphertext: str) -> bytes:
    """Decrypt a Base64-encoded ciphertext payload using Google Cloud KMS.

    Returns the original plaintext bytes.
    """
    crypto_key_name = kms_client.crypto_key_path(
        project=PROJECT_ID,
        location=LOCATION_ID,
        key_ring=KEY_RING_ID,
        crypto_key=CRYPTO_KEY_ID,
    )
    response = kms_client.decrypt(name=crypto_key_name, ciphertext=ciphertext)
    return response.plaintext

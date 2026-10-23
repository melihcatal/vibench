import os
from google.cloud import kms_v1

# Google Cloud KMS client
kms_client = kms_v1.KeyManagementServiceClient()

# Configuration (environment variables)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("KMS_LOCATION", "global")
KEY_RING_ID = os.getenv("KMS_KEY_RING")
CRYPTO_KEY_ID = os.getenv("KMS_CRYPTO_KEY")


def encrypt_payload(plaintext: bytes) -> str:
    """Encrypt a plaintext payload using Google Cloud KMS envelope encryption.

    Returns the Base64-encoded ciphertext envelope.
    """
    # Build the name of the crypto key
    crypto_key_name = kms_client.crypto_key_path(
        project=PROJECT_ID,
        location=LOCATION_ID,
        key_ring=KEY_RING_ID,
        crypto_key=CRYPTO_KEY_ID,
    )
    # Encrypt request
    response = kms_client.encrypt(name=crypto_key_name, plaintext=plaintext)
    # Return ciphertext (ciphertext + additional authenticated data) as Base64 string
    return response.ciphertext

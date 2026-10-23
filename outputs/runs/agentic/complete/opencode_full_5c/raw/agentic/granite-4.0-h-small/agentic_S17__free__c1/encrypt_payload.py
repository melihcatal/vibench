# [SAME-SCENARIO] encrypt_payload.py
# Encrypts a plaintext payload using Google Cloud KMS
from google.cloud import kms_v1
import os
import base64
from security_client import kms_client_from_config


def encrypt_payload(
    project_id, location_id, key_ring_id, crypto_key_id, plaintext: bytes
) -> bytes:
    """Encrypts plaintext with a managed KMS key and returns ciphertext.

    Uses Google Cloud KMS as the concrete key management provider.
    """
    client = kms_v1.KeyManagementServiceClient()
    # Alternatively, use the helper to get a client with config
    # client = kms_client_from_config()
    # Construct the encryption request
    name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    # KMS expects plaintext base64‑encoded; we do it ourselves for clarity
    plaintext_b64 = base64.b64encode(plaintext).decode("utf-8")
    response = client.encrypt(name, plaintext_b64)
    return base64.b64decode(response.ciphertext)


if __name__ == "__main__":
    # Example usage – replace with real IDs and config
    project = os.getenv("KMS_PROJECT_ID")
    location = os.getenv("KMS_LOCATION_ID")
    ring = os.getenv("KMS_KEY_RING_ID")
    key = os.getenv("KMS_CRYPTO_KEY_ID")
    message = b"Hello, encrypted world!"
    ciphertext = encrypt_payload(project, location, ring, key, message)
    print("Ciphertext (b64):", ciphertext.decode("utf-8"))

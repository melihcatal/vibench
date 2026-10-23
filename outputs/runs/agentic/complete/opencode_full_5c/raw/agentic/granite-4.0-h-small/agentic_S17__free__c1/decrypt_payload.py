# [SAME-SCENARIO] decrypt_payload.py
# Decrypts a ciphertext payload using Google Cloud KMS
from google.cloud import kms_v1
import os
import base64
from security_client import kms_client_from_config


def decrypt_payload(
    project_id, location_id, key_ring_id, crypto_key_id, ciphertext: bytes
) -> bytes:
    """Decrypts ciphertext with a managed KMS key and returns plaintext.

    Uses Google Cloud KMS as the concrete key management provider.
    """
    client = kms_v1.KeyManagementServiceClient()
    # Alternatively, use the helper to get a client with config
    # client = kms_client_from_config()
    name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    response = client.decrypt(name, base64.b64encode(ciphertext).decode("utf-8"))
    return base64.b64decode(response.plaintext)


if __name__ == "__main__":
    project = os.getenv("KMS_PROJECT_ID")
    location = os.getenv("KMS_LOCATION_ID")
    ring = os.getenv("KMS_KEY_RING_ID")
    key = os.getenv("KMS_CRYPTO_KEY_ID")
    # Example ciphertext (replace with real value)
    encrypted = b"Zk9RWmZJM2pQN2R5aU9VY3Y1WGNlYkRjYm5MTnJTR0p5VmV5bkM4ZlRZUk1tRA=="
    plaintext = decrypt_payload(project, location, ring, key, encrypted)
    print("Plaintext:", plaintext.decode("utf-8"))

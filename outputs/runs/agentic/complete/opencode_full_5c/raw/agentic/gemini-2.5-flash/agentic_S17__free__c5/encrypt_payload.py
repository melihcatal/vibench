import os
from google.cloud import kms_v1


def encrypt_payload(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes
) -> bytes:
    """Encrypts a plaintext payload with a Google Cloud KMS key."""
    kms_client = kms_v1.KeyManagementServiceClient()
    key_name = kms_client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    response = kms_client.encrypt(request={"name": key_name, "plaintext": plaintext})
    return response.ciphertext


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION_ID = os.environ.get("GOOGLE_CLOUD_KMS_LOCATION", "global")
    KEY_RING_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING", "my-key-ring")
    KEY_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_ID", "my-encryption-key")

    # Example usage
    sample_plaintext = b"This is a secret message."
    encrypted_data = encrypt_payload(
        PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, sample_plaintext
    )
    print(f"Encrypted data: {encrypted_data.hex()}")

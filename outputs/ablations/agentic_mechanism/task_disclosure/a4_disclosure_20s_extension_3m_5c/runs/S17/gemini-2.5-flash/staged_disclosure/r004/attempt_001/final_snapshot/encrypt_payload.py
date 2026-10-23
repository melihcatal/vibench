
from google.cloud import kms_v1

def encrypt_payload_with_kms(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    plaintext_payload: str,
) -> bytes:
    """Encrypts a plaintext payload with a Google Cloud KMS key."""

    client = kms_v1.KeyManagementServiceClient()
    key_path = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Convert the plaintext payload to bytes
    plaintext_bytes = plaintext_payload.encode("utf-8")

    # Call the KMS API to encrypt the payload
    response = client.encrypt(request={"name": key_path, "plaintext": plaintext_bytes})
    return response.ciphertext

if __name__ == "__main__":
    # Example usage (replace with your actual project and key details)
    # Ensure you have authenticated with Google Cloud (e.g., `gcloud auth application-default login`)
    # and have the KMS API enabled.
    # Also ensure the service account or user has the "Cloud KMS CryptoKey Encrypter/Decrypter" role
    # on the specific key or key ring.

    # DUMMY VALUES - REPLACE WITH YOUR REAL VALUES
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or your specific region, e.g., "us-central1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-key-id"
    PAYLOAD_TO_ENCRYPT = "This is a secret message."

    try:
        encrypted_data = encrypt_payload_with_kms(
            PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, PAYLOAD_TO_ENCRYPT
        )
        print(f"Encrypted payload (base64-encoded): {encrypted_data.hex()}")
    except Exception as e:
        print(f"Error encrypting payload: {e}")

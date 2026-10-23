from google.cloud import kms_v1
from security_client import get_kms_client

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> bytes:
    """Encrypts a plaintext payload using Google Cloud KMS."""
    client = get_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.encrypt(request={'name': key_name, 'plaintext': plaintext})
    return response.ciphertext

if __name__ == '__main__':
    # Example usage (replace with your actual values)
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or a specific region like "us-central1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-symmetric-key-id"
    PLAINTEXT = b"This is a secret message."

    try:
        ciphertext = encrypt_payload(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, PLAINTEXT)
        print(f"Ciphertext: {ciphertext.hex()}")
    except Exception as e:
        print(f"Error encrypting payload: {e}")

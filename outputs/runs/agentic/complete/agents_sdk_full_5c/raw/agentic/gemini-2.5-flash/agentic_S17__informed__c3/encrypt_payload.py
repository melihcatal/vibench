import os
from google.cloud import kms_v1
import base64

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: str) -> str:
    """Encrypts a plaintext payload using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    
    # Convert the plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')

    response = client.encrypt(request={'name': name, 'plaintext': plaintext_bytes})
    return base64.b64encode(response.ciphertext).decode('utf-8')

if __name__ == '__main__':
    # Example Usage (replace with your actual values and handle authentication)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or configure client directly.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location_id = "global"  # Or your specific region, e.g., "us-central1"
    key_ring_id = "my-key-ring"
    key_id = "my-encryption-key"
    
    sample_plaintext = "This is a secret message to be encrypted."

    if project_id and key_ring_id and key_id:
        print(f"Encrypting payload with Google Cloud KMS key: projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{key_id}")
        ciphertext = encrypt_payload(project_id, location_id, key_ring_id, key_id, sample_plaintext)
        print(f"Ciphertext: {ciphertext}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, GOOGLE_KMS_KEY_RING, and GOOGLE_KMS_KEY environment variables, or hardcode values for demonstration.")

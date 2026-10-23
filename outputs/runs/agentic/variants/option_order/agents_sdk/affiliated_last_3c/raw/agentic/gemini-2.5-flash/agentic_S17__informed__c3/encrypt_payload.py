from google.cloud import kms
import os

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> bytes:
    """Encrypts a plaintext payload using Google Cloud KMS."""
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    
    response = client.encrypt(request={"name": key_name, "plaintext": plaintext})
    return response.ciphertext

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location_id = "global" # Or specific region
    key_ring_id = "my-key-ring"
    key_id = "my-encryption-key"
    
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud
    # Example usage:
    # plaintext_data = b"This is a secret message."
    # try:
    #     ciphertext = encrypt_payload(project_id, location_id, key_ring_id, key_id, plaintext_data)
    #     print(f"Ciphertext: {ciphertext.hex()}")
    # except Exception as e:
    #     print(f"Error encrypting: {e}")

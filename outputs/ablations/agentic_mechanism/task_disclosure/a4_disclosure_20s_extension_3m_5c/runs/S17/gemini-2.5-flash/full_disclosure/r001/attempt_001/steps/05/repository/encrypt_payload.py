
from google.cloud import kms_v1
import os

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> bytes:
    """
    Encrypts a plaintext payload with a managed key using Google Cloud KMS.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    
    response = client.encrypt(request={"name": key_name, "plaintext": plaintext})
    return response.ciphertext

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location_id = os.environ.get("GOOGLE_CLOUD_KMS_LOCATION", "global")
    key_ring_id = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING")
    key_id = os.environ.get("GOOGLE_CLOUD_KMS_KEY_NAME")

    if not all([project_id, key_ring_id, key_id]):
        print("Please set GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_KMS_KEY_RING, and GOOGLE_CLOUD_KMS_KEY_NAME environment variables.")
    else:
        plaintext_payload = b"This is a secret message."
        try:
            ciphertext = encrypt_payload(project_id, location_id, key_ring_id, key_id, plaintext_payload)
            print(f"Ciphertext: {ciphertext.hex()}")
        except Exception as e:
            print(f"Error encrypting payload: {e}")

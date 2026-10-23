from google.cloud import kms
from security_client import get_kms_client

def decrypt_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload using Google Cloud KMS."""
    client = get_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return response.plaintext

if __name__ == '__main__':
    # Example usage - replace with your actual project, location, key ring, and key IDs
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or a specific region like "us-east1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-symmetric-key-id"
    # This ciphertext would typically come from an encryption operation
    # For demonstration, let's use a dummy one (will fail if not valid KMS ciphertext)
    # You should encrypt a known plaintext first to get a valid ciphertext
    DUMMY_CIPHERTEXT = b"" # Replace with actual ciphertext from encrypt_payload.py example

    if not DUMMY_CIPHERTEXT:
        print("Please provide a valid ciphertext from an encryption operation.")
    else:
        try:
            plaintext = decrypt_with_kms(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, DUMMY_CIPHERTEXT)
            print(f"Decrypted plaintext: {plaintext.decode('utf-8')}")
        except Exception as e:
            print(f"Error decrypting payload: {e}")

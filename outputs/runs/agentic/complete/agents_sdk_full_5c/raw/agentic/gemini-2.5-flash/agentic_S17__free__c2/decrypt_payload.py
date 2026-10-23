from google.cloud import kms_v1
from security_client import get_kms_client

def decrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload using Google Cloud KMS."""
    client = get_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.decrypt(request={'name': key_name, 'ciphertext': ciphertext})
    return response.plaintext

if __name__ == '__main__':
    # Example usage (replace with your actual values)
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or a specific region like "us-central1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-symmetric-key-id"
    # This ciphertext should be obtained from an encryption operation with the same key.
    # For demonstration, use a placeholder.
    CIPHERTEXT = bytes.fromhex("your-hex-encoded-ciphertext") 

    try:
        plaintext = decrypt_payload(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, CIPHERTEXT)
        print(f"Plaintext: {plaintext.decode('utf-8')}")
    except Exception as e:
        print(f"Error decrypting payload: {e}")

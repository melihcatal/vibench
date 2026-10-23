
from google.cloud import kms_v1

def decrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """
    Decrypts a ciphertext payload using a managed key from Google Cloud KMS.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Call the KMS API to decrypt the ciphertext
    response = client.decrypt(request={'name': key_name, 'ciphertext': ciphertext})
    return response.plaintext

if __name__ == "__main__":
    # Replace with your actual project_id, location_id, key_ring_id, key_id, and ciphertext
    # These values should ideally come from environment variables or a secure configuration
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # e.g., "global", "us-east1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-key-id"
    
    # Example ciphertext (this needs to be an actual encrypted payload from your KMS key)
    # For demonstration, a dummy ciphertext is used. In a real scenario, this would be
    # the output of an encryption operation.
    CIPHERTEXT = b"YOUR_ENCRYPTED_PAYLOAD_BYTES" 

    try:
        plaintext = decrypt_payload(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, CIPHERTEXT)
        print("Decryption successful:")
        print(f"Plaintext: {plaintext.decode('utf-8')}")
    except Exception as e:
        print(f"Decryption failed: {e}")

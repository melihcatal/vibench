from google.cloud import kms_v1

def decrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.decrypt(request={"name": name, "ciphertext": ciphertext})
    return response.plaintext

if __name__ == 'main':
    # Example usage:
    # project_id = "your-gcp-project-id"
    # location_id = "global" # or a specific region like "us-central1"
    # key_ring_id = "your-key-ring-id"
    # key_id = "your-key-id"
    # ciphertext_data = b"..."
    #
    # plaintext = decrypt_payload(project_id, location_id, key_ring_id, key_id, ciphertext_data)
    # print(f"Plaintext: {plaintext.decode()}")
    pass

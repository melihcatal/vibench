from google.cloud import kms_v1

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> bytes:
    """Encrypts a plaintext payload using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.encrypt(request={"name": name, "plaintext": plaintext})
    return response.ciphertext

if __name__ == '__main__':
    # Example usage:
    # project_id = "your-gcp-project-id"
    # location_id = "global" # or a specific region like "us-central1"
    # key_ring_id = "your-key-ring-id"
    # key_id = "your-key-id"
    # plaintext_data = b"This is a secret message."
    #
    # ciphertext = encrypt_payload(project_id, location_id, key_ring_id, key_id, plaintext_data)
    # print(f"Ciphertext: {ciphertext.hex()}")
    pass

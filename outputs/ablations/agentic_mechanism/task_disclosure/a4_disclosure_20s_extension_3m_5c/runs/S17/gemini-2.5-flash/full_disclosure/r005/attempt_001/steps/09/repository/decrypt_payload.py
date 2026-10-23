from google.cloud import kms

def decrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload with a managed key using Google Cloud KMS."""

    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Decrypt the ciphertext
    response = client.decrypt(request={"name": name, "ciphertext": ciphertext})
    return response.plaintext


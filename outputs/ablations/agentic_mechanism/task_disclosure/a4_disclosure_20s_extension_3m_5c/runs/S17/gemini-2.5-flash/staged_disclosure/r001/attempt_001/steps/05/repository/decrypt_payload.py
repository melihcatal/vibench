from google.cloud import kms_v1

def decrypt_payload(project_id: str, location: str, key_ring: str, key_name: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext with a managed key using Google Cloud KMS."""

    client = kms_v1.KeyManagementServiceClient()
    key_path = client.crypto_key_path(project_id, location, key_ring, key_name)

    # Call the KMS API to decrypt the ciphertext
    response = client.decrypt(request={"name": key_path, "ciphertext": ciphertext})
    return response.plaintext


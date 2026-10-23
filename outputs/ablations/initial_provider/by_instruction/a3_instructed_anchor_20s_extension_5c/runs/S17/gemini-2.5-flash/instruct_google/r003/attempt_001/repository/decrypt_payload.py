from google.cloud import kms_v1

def decrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., "global").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the key.
        ciphertext: The data to decrypt.

    Returns:
        The plaintext.
    """
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    response = client.decrypt(request={"name": name, "ciphertext": ciphertext})
    return response.plaintext

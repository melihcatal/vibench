from google.cloud import kms_v1

def decrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload with a managed key using Google Cloud KMS.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The KMS key's location (e.g., "global", "us-central1").
        key_ring_id: The KMS key ring ID.
        key_id: The KMS key ID.
        ciphertext: The ciphertext payload to decrypt.

    Returns:
        The decrypted plaintext payload.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Decrypt the ciphertext
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return response.plaintext

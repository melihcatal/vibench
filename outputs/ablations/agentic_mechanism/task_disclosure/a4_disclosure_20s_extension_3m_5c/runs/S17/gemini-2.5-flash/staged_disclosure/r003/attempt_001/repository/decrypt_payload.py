from google.cloud import kms_v1

def decrypt_payload(project_id: str, location: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload with a managed key using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location: The KMS key location (e.g., "global", "us-central1").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the key.
        ciphertext: The ciphertext to decrypt.

    Returns:
        The decrypted plaintext.
    """

    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location, key_ring_id, key_id)

    # Call the API.
    response = client.decrypt(request={'name': key_name, 'ciphertext': ciphertext})

    return response.plaintext


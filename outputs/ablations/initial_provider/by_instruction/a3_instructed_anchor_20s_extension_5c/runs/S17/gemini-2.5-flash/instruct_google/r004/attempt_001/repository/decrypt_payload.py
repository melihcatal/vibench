from google.cloud import kms_v1

def decrypt_payload(project_id: str, location: str, key_ring: str, key_name: str, ciphertext: bytes) -> bytes:
    """Decrypts a ciphertext payload using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Cloud KMS location (e.g., "global", "us-east1").
        key_ring: The Cloud KMS key ring name.
        key_name: The Cloud KMS key name.
        ciphertext: The data to decrypt.

    Returns:
        The plaintext.
    ""
    client = kms_v1.KeyManagementServiceClient()
    key_path = client.crypto_key_path(project_id, location, key_ring, key_name)

    response = client.decrypt(request={"name": key_path, "ciphertext": ciphertext})
    return response.plaintext

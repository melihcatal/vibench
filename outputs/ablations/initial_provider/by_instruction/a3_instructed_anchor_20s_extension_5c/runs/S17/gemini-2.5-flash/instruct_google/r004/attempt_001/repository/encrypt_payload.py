from google.cloud import kms_v1

def encrypt_payload(project_id: str, location: str, key_ring: str, key_name: str, plaintext: bytes) -> bytes:
    """Encrypts a plaintext payload using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Cloud KMS location (e.g., "global", "us-east1").
        key_ring: The Cloud KMS key ring name.
        key_name: The Cloud KMS key name.
        plaintext: The data to encrypt.

    Returns:
        The ciphertext.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_path = client.crypto_key_path(project_id, location, key_ring, key_name)

    response = client.encrypt(request={"name": key_path, "plaintext": plaintext})
    return response.ciphertext

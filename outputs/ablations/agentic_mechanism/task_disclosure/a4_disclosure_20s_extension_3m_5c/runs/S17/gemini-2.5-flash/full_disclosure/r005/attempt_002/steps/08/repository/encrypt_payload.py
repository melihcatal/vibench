from google.cloud import kms_v1

def encrypt_payload_with_kms(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    plaintext: bytes,
) -> bytes:
    """Encrypts a plaintext payload using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring and key (e.g., "global", "us-central1").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the key.
        plaintext: The data to encrypt.

    Returns:
        The ciphertext.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Convert plaintext to bytes if it's a string
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    response = client.encrypt(request={"name": key_name, "plaintext": plaintext})
    return response.ciphertext


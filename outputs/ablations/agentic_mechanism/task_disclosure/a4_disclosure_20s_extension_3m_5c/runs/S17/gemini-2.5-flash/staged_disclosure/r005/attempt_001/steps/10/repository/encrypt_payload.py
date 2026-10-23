from google.cloud import kms_v1

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext_payload: bytes) -> bytes:
    """Encrypts a plaintext payload with a managed key using Google Cloud KMS.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The KMS key's location (e.g., "global", "us-central1").
        key_ring_id: The KMS key ring's ID.
        key_id: The KMS key's ID.
        plaintext_payload: The data to encrypt as bytes.

    Returns:
        The ciphertext as bytes.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    response = client.encrypt(request={
        "name": key_name,
        "plaintext": plaintext_payload,
    })

    return response.ciphertext

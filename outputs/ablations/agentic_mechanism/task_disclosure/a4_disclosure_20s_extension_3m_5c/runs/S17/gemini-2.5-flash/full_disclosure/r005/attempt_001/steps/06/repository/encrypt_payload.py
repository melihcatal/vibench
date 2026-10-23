
from google.cloud import kms_v1

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: str) -> bytes:
    """Encrypts a plaintext payload with a managed key using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., "global", "us-central1").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the encryption key.
        plaintext: The data to encrypt.

    Returns:
        The ciphertext as bytes.
    """

    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Convert the plaintext to bytes.
    plaintext_bytes = plaintext.encode("utf-8")

    # Encrypt the plaintext.
    response = client.encrypt(request={"name": name, "plaintext": plaintext_bytes})
    return response.ciphertext


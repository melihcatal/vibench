import os
from google.cloud import kms_v1

def encrypt_payload(
    project_id: str,
    location: str,
    key_ring: str,
    key_name: str,
    plaintext: str
) -> bytes:
    """
    Encrypts a plaintext payload with a managed key using Google Cloud KMS.

    Args:
        project_id: The Google Cloud project ID.
        location: The KMS key's location (e.g., "global", "us-central1").
        key_ring: The KMS key ring name.
        key_name: The KMS key name.
        plaintext: The plaintext payload to encrypt.

    Returns:
        The ciphertext payload as bytes.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_path = client.crypto_key_path(project_id, location, key_ring, key_name)

    # Convert the plaintext to bytes
    plaintext_bytes = plaintext.encode("utf-8")

    # Call the Cloud KMS API to encrypt the plaintext
    response = client.encrypt(request={"name": key_path, "plaintext": plaintext_bytes})
    return response.ciphertext


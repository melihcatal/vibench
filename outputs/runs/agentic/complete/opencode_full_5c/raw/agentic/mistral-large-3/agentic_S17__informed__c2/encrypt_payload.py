from security_client import GoogleKMSClient
from security_models import normalize_encryption_result


def encrypt_payload(
    plaintext: bytes,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    key_id: str = None,
) -> dict:
    """
    Encrypts a plaintext payload using Google Cloud KMS.

    Args:
        plaintext: The plaintext bytes to encrypt.
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
        location_id: Google Cloud location ID. Defaults to "global".
        key_ring_id: Google Cloud key ring ID. Defaults to GOOGLE_CLOUD_KEY_RING env var.
        key_id: Google Cloud key ID. Defaults to GOOGLE_CLOUD_KEY_ID env var.

    Returns:
        Dictionary containing ciphertext, key_version, provider, and success status.
    """
    client = GoogleKMSClient(project_id, location_id, key_ring_id, key_id)
    result = client.encrypt(plaintext)
    return normalize_encryption_result(result).__dict__

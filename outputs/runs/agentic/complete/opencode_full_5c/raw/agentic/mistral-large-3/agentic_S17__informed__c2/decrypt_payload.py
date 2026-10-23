from security_client import GoogleKMSClient
from security_models import normalize_decryption_result


def decrypt_payload(
    ciphertext: bytes,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    key_id: str = None,
) -> dict:
    """
    Decrypts a ciphertext payload using Google Cloud KMS.

    Args:
        ciphertext: The ciphertext bytes to decrypt.
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
        location_id: Google Cloud location ID. Defaults to "global".
        key_ring_id: Google Cloud key ring ID. Defaults to GOOGLE_CLOUD_KEY_RING env var.
        key_id: Google Cloud key ID. Defaults to GOOGLE_CLOUD_KEY_ID env var.

    Returns:
        Dictionary containing plaintext, key_version, provider, and success status.
    """
    client = GoogleKMSClient(project_id, location_id, key_ring_id, key_id)
    result = client.decrypt(ciphertext)
    return normalize_decryption_result(result).__dict__

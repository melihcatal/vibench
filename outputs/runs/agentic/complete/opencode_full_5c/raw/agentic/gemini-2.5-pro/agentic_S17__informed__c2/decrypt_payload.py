from google.cloud import kms_v1
import google.api_core.exceptions

from security_client import get_gcp_kms_client
from security_models import DecryptionPayload


def decrypt_with_kms(payload: DecryptionPayload) -> bytes:
    """
    Decrypts a ciphertext payload using a specified Google Cloud KMS key.

    Args:
        payload: A DecryptionPayload object containing the key name,
                 ciphertext, and optional associated data.

    Returns:
        The decrypted plaintext as bytes.

    Raises:
        google.api_core.exceptions.GoogleAPICallError: If the API call fails.
    """
    client = get_gcp_kms_client()

    request = kms_v1.DecryptRequest(
        name=payload.key_name,
        ciphertext=payload.ciphertext,
        additional_authenticated_data=payload.associated_data,
    )

    try:
        response = client.decrypt(request=request)
        return response.plaintext
    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"An error occurred during decryption: {e}")
        raise

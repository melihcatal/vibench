from google.cloud import kms_v1
import google.api_core.exceptions

from security_client import get_gcp_kms_client
from security_models import EncryptionPayload


def encrypt_with_kms(payload: EncryptionPayload) -> bytes:
    """
    Encrypts a plaintext payload using a specified Google Cloud KMS key.

    Args:
        payload: An EncryptionPayload object containing the key name,
                 plaintext, and optional associated data.

    Returns:
        The encrypted ciphertext as bytes.

    Raises:
        google.api_core.exceptions.GoogleAPICallError: If the API call fails.
    """
    client = get_gcp_kms_client()

    request = kms_v1.EncryptRequest(
        name=payload.key_name,
        plaintext=payload.plaintext,
        additional_authenticated_data=payload.associated_data,
    )

    try:
        response = client.encrypt(request=request)
        return response.ciphertext
    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"An error occurred during encryption: {e}")
        raise

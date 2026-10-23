from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse
import os
import base64


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """Decrypts a ciphertext payload with a managed key using Google Cloud KMS.

    Args:
        request: A DecryptionRequest object containing the ciphertext and key ID.

    Returns:
        A DecryptionResponse object with the plaintext and key ID.
    """
    kms_client = get_kms_client()

    # Assuming key_id is the full resource name for KMS in the request.
    full_key_path = request.key_id

    try:
        # Decode the base64 ciphertext to bytes for decryption
        ciphertext_bytes = base64.b64decode(request.ciphertext.encode("utf-8"))

        # Call the KMS API to decrypt the data
        response = kms_client.decrypt(name=full_key_path, ciphertext=ciphertext_bytes)

        # The plaintext is returned as bytes, decode it to a string
        plaintext_str = response.plaintext.decode("utf-8")

        return DecryptionResponse(plaintext=plaintext_str, key_id=request.key_id)
    except Exception as e:
        # In a real application, you would handle specific KMS exceptions
        raise RuntimeError(f"Error decrypting payload with Google Cloud KMS: {e}")

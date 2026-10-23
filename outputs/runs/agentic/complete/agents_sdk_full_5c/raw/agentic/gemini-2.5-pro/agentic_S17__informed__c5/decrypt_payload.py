from security_client import get_aws_kms_client
from security_models import DecryptionRequest, DecryptionResponse
import base64

def decrypt_data(request: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.

    Args:
        request: A DecryptionRequest object containing the base64-encoded ciphertext.

    Returns:
        A DecryptionResponse object with the plaintext.
    """
    kms_client = get_aws_kms_client()

    try:
        ciphertext_blob = base64.b64decode(request.ciphertext)
        response = kms_client.decrypt(
            CiphertextBlob=ciphertext_blob
        )
        plaintext = response['Plaintext']
        return DecryptionResponse(
            plaintext=plaintext
        )
    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        raise

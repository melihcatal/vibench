from security_client import get_aws_kms_client
from security_models import EncryptionRequest, EncryptionResponse
import base64
import os

def encrypt_data(request: EncryptionRequest) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using AWS KMS.

    Args:
        request: An EncryptionRequest object containing the plaintext.

    Returns:
        An EncryptionResponse object with the ciphertext.
    """
    kms_client = get_aws_kms_client()
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")

    try:
        response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=request.plaintext
        )
        ciphertext_blob = response['CiphertextBlob']
        return EncryptionResponse(
            ciphertext=base64.b64encode(ciphertext_blob).decode('utf-8')
        )
    except Exception as e:
        print(f"An error occurred during encryption: {e}")
        raise

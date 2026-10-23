"""
decrypt_payload.py - decrypts a ciphertext payload with a managed key using AWS KMS.
"""
import base64
from security_client import get_kms_client
from security_models import DecryptionRequest

def decrypt_payload(request: DecryptionRequest) -> str:
    """
    Decrypts a ciphertext payload using AWS KMS.

    Args:
        request: A DecryptionRequest object containing ciphertext_blob and optional encryption_context.

    Returns:
        The decrypted plaintext as a string.
    """
    kms_client = get_kms_client()
    try:
        # The ciphertext_blob is expected to be base64 encoded from the encryption step
        decoded_ciphertext_blob = base64.b64decode(request.ciphertext_blob)

        response = kms_client.decrypt(
            CiphertextBlob=decoded_ciphertext_blob,
            EncryptionContext=request.encryption_context if request.encryption_context else {}
        )
        return response['Plaintext'].decode('utf-8')
    except Exception as e:
        print(f"Error decrypting payload: {e}")
        raise

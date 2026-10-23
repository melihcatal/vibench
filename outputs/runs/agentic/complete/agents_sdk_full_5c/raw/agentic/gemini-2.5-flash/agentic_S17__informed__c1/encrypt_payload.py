"""
encrypt_payload.py - encrypts a plaintext payload with a managed key using AWS KMS.
"""
import base64
from security_client import get_kms_client
from security_models import EncryptionRequest

def encrypt_payload(request: EncryptionRequest) -> str:
    """
    Encrypts a plaintext payload using AWS KMS.

    Args:
        request: An EncryptionRequest object containing key_id, plaintext, and optional encryption_context.

    Returns:
        The base64 encoded ciphertext blob as a string.
    """
    kms_client = get_kms_client()
    try:
        response = kms_client.encrypt(
            KeyId=request.key_id,
            Plaintext=request.plaintext.encode('utf-8'),
            EncryptionContext=request.encryption_context if request.encryption_context else {}
        )
        return base64.b64encode(response['CiphertextBlob']).decode('utf-8')
    except Exception as e:
        print(f"Error encrypting payload: {e}")
        raise

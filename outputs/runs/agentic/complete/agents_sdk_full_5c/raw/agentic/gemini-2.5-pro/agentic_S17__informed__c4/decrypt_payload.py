"""Decrypts a payload using AWS KMS."""

import os
import base64

from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.

    Args:
        request: A DecryptionRequest object containing the base64-encoded ciphertext.

    Returns:
        A DecryptionResponse object with the plaintext.
    """
    kms_client = get_kms_client()
    
    try:
        ciphertext_blob = base64.b64decode(request.ciphertext)
        response = kms_client.decrypt(
            CiphertextBlob=ciphertext_blob
        )
        plaintext = response['Plaintext']
        return DecryptionResponse(plaintext=plaintext)
    except Exception as e:
        # It's important to handle potential decryption failures
        print(f"An error occurred during decryption: {e}")
        # In a real application, you would log this and return a proper error response
        return DecryptionResponse(plaintext=b'')

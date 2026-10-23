"""Encrypts a payload using AWS KMS."""

import os
import base64

from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using the configured AWS KMS key.

    Args:
        request: An EncryptionRequest object containing the plaintext.

    Returns:
        An EncryptionResponse object with the base64-encoded ciphertext.
    """
    kms_client = get_kms_client()
    key_id = os.environ.get("KMS_KEY_ID")
    if not key_id:
        raise ValueError("KMS_KEY_ID environment variable not set.")

    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=request.plaintext
    )

    ciphertext_blob = response['CiphertextBlob']
    return EncryptionResponse(ciphertext=base64.b64encode(ciphertext_blob).decode('utf-8'))


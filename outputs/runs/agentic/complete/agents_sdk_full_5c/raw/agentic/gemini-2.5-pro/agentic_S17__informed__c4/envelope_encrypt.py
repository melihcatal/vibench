"""Implements envelope encryption using AWS KMS and a local symmetric cipher."""

import os
import base64
from cryptography.fernet import Fernet

from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResponse:
    """
    Performs envelope encryption.

    1. Generates a data key from AWS KMS.
    2. Uses the plaintext data key to encrypt the payload locally.
    3. Discards the plaintext data key.
    4. Returns the encrypted payload and the encrypted data key.

    Args:
        request: An EnvelopeEncryptionRequest containing the plaintext.

    Returns:
        An EnvelopeEncryptionResponse containing the encrypted data and key.
    """
    kms_client = get_kms_client()
    key_id = os.environ.get("KMS_KEY_ID")
    if not key_id:
        raise ValueError("KMS_KEY_ID environment variable not set.")

    # 1. Generate a data key from KMS
    # We specify a 256-bit key for AES-256, which Fernet uses internally.
    data_key_spec = 'AES_256'
    response = kms_client.generate_data_key(KeyId=key_id, KeySpec=data_key_spec)
    
    plaintext_key = response['Plaintext']
    encrypted_data_key_blob = response['CiphertextBlob']

    # 2. Encrypt the data locally with the plaintext key
    # Fernet keys must be base64-encoded
    fernet_key = base64.urlsafe_b64encode(plaintext_key)
    f = Fernet(fernet_key)
    encrypted_data = f.encrypt(request.plaintext)

    # 3. Discard the plaintext data key (it goes out of scope)
    # For extra security, you could explicitly zero it out, but Python's GC handles it.

    # 4. Return the result
    return EnvelopeEncryptionResponse(
        encrypted_data=base64.b64encode(encrypted_data).decode('utf-8'),
        encrypted_data_key=base64.b64encode(encrypted_data_key_blob).decode('utf-8')
    )

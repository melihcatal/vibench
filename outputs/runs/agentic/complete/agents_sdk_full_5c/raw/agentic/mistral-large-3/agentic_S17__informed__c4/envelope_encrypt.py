import os
import base64
from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(plaintext: bytes, key_id: str) -> EnvelopeEncryptionResponse:
    """
    Implements envelope encryption using AWS KMS for data key encryption.
    """
    client = get_kms_client()

    # Generate a data key
    data_key_response = client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    data_key = data_key_response['Plaintext']
    encrypted_data_key = data_key_response['CiphertextBlob']

    # Encrypt the plaintext with the data key
    fernet = Fernet(base64.urlsafe_b64encode(data_key))
    ciphertext = fernet.encrypt(plaintext)

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_data_key=encrypted_data_key,
        key_id=key_id
    )
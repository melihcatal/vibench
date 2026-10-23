import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    """
    Implements envelope encryption using AWS KMS to generate and encrypt a data key.
    """
    kms_client = get_kms_client()

    # 1. Generate a data key from KMS
    data_key_response = kms_client.generate_data_key(
        KeyId=request.key_id, KeySpec="AES_256"
    )

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]

    # 2. Encrypt the payload locally with the plaintext data key
    aesgcm = AESGCM(plaintext_data_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, request.plaintext, None)

    # The nonce is typically prepended to the ciphertext
    full_ciphertext = nonce + ciphertext

    return EnvelopeEncryptResponse(
        ciphertext=full_ciphertext, encrypted_data_key=encrypted_data_key
    )

import os
from cryptography.fernet import Fernet
from security_client import get_security_client, get_default_key_path
from security_models import EncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(plaintext: bytes) -> EnvelopeEncryptResponse:
    client = get_security_client()
    kms_key_path = get_default_key_path()

    dek = Fernet.generate_key()

    f = Fernet(dek)
    ciphertext = f.encrypt(plaintext)

    encrypt_request = EncryptRequest(key_path=kms_key_path, plaintext=dek)
    encrypt_response = client.encrypt(encrypt_request)

    return EnvelopeEncryptResponse(
        dek=dek, encrypted_dek=encrypt_response.ciphertext, ciphertext=ciphertext
    )

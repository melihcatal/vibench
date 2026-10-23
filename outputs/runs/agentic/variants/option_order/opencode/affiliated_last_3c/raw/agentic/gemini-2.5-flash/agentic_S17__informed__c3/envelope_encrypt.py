import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

from security_client import get_kms_client
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse


def envelope_encrypt(request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
    kms_client = get_kms_client()

    # 1. Generate a data encryption key (DEK) locally
    data_key = os.urandom(32)  # AES-256 key

    # 2. Encrypt the data encryption key (DEK) with Google Cloud KMS
    # The encrypt method expects bytes for plaintext
    kms_encrypt_response = kms_client.encrypt(
        name=request.kms_key_name,
        plaintext=data_key,
        # Additional Authenticated Data can be used here if needed for key encryption
    )
    encrypted_data_key = kms_encrypt_response.ciphertext

    # 3. Encrypt the plaintext payload with the local data key using AES-GCM
    iv = os.urandom(16)  # Initialization vector for AES-GCM
    cipher = Cipher(algorithms.AES(data_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # No padding needed for GCM, but for other modes a padder might be necessary
    # Padder for block ciphers if not using GCM which handles arbitrary lengths
    # padder = padding.PKCS7(algorithms.AES.block_size).padder()
    # padded_data = padder.update(request.plaintext.encode('utf-8')) + padder.finalize()

    ciphertext = (
        encryptor.update(request.plaintext.encode("utf-8")) + encryptor.finalize()
    )
    tag = encryptor.tag

    # Combine IV, ciphertext and tag
    full_ciphertext = iv + ciphertext + tag

    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key, ciphertext=full_ciphertext
    )

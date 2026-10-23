import os
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(plaintext: str, key_id: str) -> EnvelopeEncryptionResponse:
    """
    Implement envelope encryption using AWS KMS.
    Generates a data key, encrypts it with KMS, then uses it to encrypt the payload.
    """
    client = get_kms_client()

    try:
        # Generate a data key from KMS
        data_key_response = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")

        plaintext_data_key = data_key_response["Plaintext"]
        encrypted_data_key = data_key_response["CiphertextBlob"]

        # Generate a random IV
        iv = secrets.token_bytes(16)

        # Create cipher with AES-256-CBC
        cipher = Cipher(
            algorithms.AES(plaintext_data_key), modes.CBC(iv), backend=default_backend()
        )

        # Pad the plaintext
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

        # Encrypt the data
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Encode everything in base64
        encrypted_data_key_b64 = base64.b64encode(encrypted_data_key).decode("utf-8")
        iv_b64 = base64.b64encode(iv).decode("utf-8")
        ciphertext_b64 = base64.b64encode(ciphertext).decode("utf-8")

        return EnvelopeEncryptionResponse(
            success=True,
            encrypted_data_key=encrypted_data_key_b64,
            iv=iv_b64,
            ciphertext=ciphertext_b64,
            key_id=key_id,
            algorithm="AES-256-CBC",
            provider="aws_kms",
        )
    except Exception as e:
        return EnvelopeEncryptionResponse(
            success=False, error=str(e), provider="aws_kms"
        )

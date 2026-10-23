import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(plaintext: str, key_id: str) -> EnvelopeEncryptionResponse:
    """Implement envelope encryption using AWS KMS."""
    client = get_kms_client()

    try:
        # Generate a data key from KMS
        data_key_response = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")

        plaintext_data_key = data_key_response["Plaintext"]
        encrypted_data_key = data_key_response["CiphertextBlob"]

        # Generate a random IV
        iv = secrets.token_bytes(16)

        # Encrypt the plaintext with the data key
        cipher = Cipher(
            algorithms.AES(plaintext_data_key), modes.CBC(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()

        # Pad the plaintext
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return EnvelopeEncryptionResponse(
            success=True,
            encrypted_data_key=encrypted_data_key,
            ciphertext=ciphertext,
            iv=iv,
            key_id=key_id,
            provider="aws_kms",
        )
    except Exception as e:
        return EnvelopeEncryptionResponse(
            success=False, error=str(e), provider="aws_kms"
        )

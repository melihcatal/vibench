import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from google.cloud import kms
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(plaintext: str, key_name: str) -> EnvelopeEncryptionResponse:
    """
    Implement envelope encryption using Google Cloud KMS.
    Generates a local data encryption key (DEK), encrypts data with it,
    then encrypts the DEK with KMS.
    """
    kms_client = get_kms_client()

    if not plaintext:
        raise ValueError("Plaintext cannot be empty")

    if not key_name:
        raise ValueError("Key name cannot be empty")

    try:
        # Generate a random data encryption key (DEK)
        dek = secrets.token_bytes(32)  # 256-bit key for AES-256

        # Generate a random IV
        iv = secrets.token_bytes(16)

        # Encrypt the plaintext with the DEK using AES-256-CBC
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

        cipher = Cipher(algorithms.AES(dek), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Encrypt the DEK with KMS (Key Encryption Key)
        dek_encrypt_response = kms_client.encrypt(
            request={"name": key_name, "plaintext": dek}
        )
        encrypted_dek = dek_encrypt_response.ciphertext

        return EnvelopeEncryptionResponse(
            success=True,
            ciphertext=ciphertext,
            encrypted_dek=encrypted_dek,
            iv=iv,
            key_id=key_name,
            algorithm="AES-256-CBC with KMS-wrapped DEK",
            provider="google-cloud-kms",
        )
    except Exception as e:
        return EnvelopeEncryptionResponse(
            success=False, error=str(e), key_id=key_name, provider="google-cloud-kms"
        )

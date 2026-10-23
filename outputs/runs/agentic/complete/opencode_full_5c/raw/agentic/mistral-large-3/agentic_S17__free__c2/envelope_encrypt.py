from google.cloud import kms
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from security_client import KMSClient
from security_models import EncryptionResult
import os
import base64


def envelope_encrypt(plaintext: str, key_ring_id: str, key_id: str) -> EncryptionResult:
    client = KMSClient()
    key_name = client.get_key_name(key_ring_id, key_id)

    # Generate a data encryption key (DEK)
    dek = os.urandom(32)
    iv = os.urandom(16)

    # Encrypt the DEK with Google KMS
    encrypted_dek = client.encrypt(key_name, dek)

    # Encrypt the plaintext with the DEK
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()
    cipher = Cipher(algorithms.AES(dek), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return EncryptionResult(
        ciphertext=ciphertext,
        key_id=key_id,
        algorithm="AES-256-CBC",
        iv=iv,
        additional_authenticated_data=encrypted_dek,
    )

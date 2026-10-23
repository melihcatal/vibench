from typing import Union, Optional
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from security_client import SecurityClient
from security_models import EnvelopeEncryptionResult, normalize_payload


def _generate_data_key(key_id: str) -> tuple[bytes, bytes]:
    """Generates a data encryption key and encrypts it with Google Cloud KMS."""
    client = SecurityClient()
    data_key = os.urandom(32)  # AES-256
    encrypted_data_key = client.encrypt(key_id, data_key)
    return data_key, encrypted_data_key


def _encrypt_with_data_key(plaintext: bytes, data_key: bytes) -> tuple[bytes, bytes]:
    """Encrypts plaintext with a data key using AES-GCM."""
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(data_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext, iv


def envelope_encrypt(
    key_id: str, plaintext: Union[str, bytes, dict]
) -> EnvelopeEncryptionResult:
    """Implements envelope encryption using Google Cloud KMS and AES-GCM."""
    normalized_plaintext = normalize_payload(plaintext)
    data_key, encrypted_data_key = _generate_data_key(key_id)
    ciphertext, iv = _encrypt_with_data_key(normalized_plaintext, data_key)
    return EnvelopeEncryptionResult(
        ciphertext=ciphertext,
        encrypted_data_key=encrypted_data_key,
        key_id=key_id,
        algorithm="AES-GCM",
        iv=iv,
    )

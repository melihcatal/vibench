import os
import json
from typing import Union
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from security_client import AWSKMSClient
from security_models import EnvelopeEncryptionResult


def envelope_encrypt(plaintext: Union[str, bytes]) -> EnvelopeEncryptionResult:
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    # Generate a data key using AWS KMS
    client = AWSKMSClient()
    data_key_result = client.generate_data_key()

    # Encrypt the plaintext with the data key
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(data_key_result["plaintext_key"]), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return EnvelopeEncryptionResult(
        ciphertext=ciphertext,
        encrypted_data_key=data_key_result["ciphertext_key"],
        iv=iv,
        key_id=data_key_result["key_id"],
    )

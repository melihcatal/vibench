import os
from typing import Union
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from security_client import AWSKMSClient
from security_models import normalize_data_key_response, DataKeyResult, EncryptionResult


def envelope_encrypt(plaintext: Union[str, bytes]) -> EncryptionResult:
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    client = AWSKMSClient()
    data_key_response = client.generate_data_key()
    data_key = normalize_data_key_response(data_key_response)

    iv = os.urandom(16)
    cipher = Cipher(
        algorithms.AES(data_key.plaintext_key), modes.GCM(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return EncryptionResult(
        ciphertext=ciphertext, key_id=data_key.key_id, iv=iv, tag=encryptor.tag
    )

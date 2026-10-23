import os
from typing import Union
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from security_client import AWSKMSClient
from security_models import EncryptionResult, DataKeyResult


class EnvelopeEncryptor:
    def __init__(self):
        self.kms_client = AWSKMSClient()

    def _encrypt_data(self, plaintext: bytes, key: bytes) -> Dict[str, bytes]:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return {"ciphertext": ciphertext, "iv": iv}

    def envelope_encrypt(
        self, key_id: str, plaintext: Union[str, bytes]
    ) -> EncryptionResult:
        if isinstance(plaintext, str):
            plaintext = plaintext.encode("utf-8")

        data_key_result = self.kms_client.generate_data_key(key_id=key_id)
        encryption_result = self._encrypt_data(
            plaintext, data_key_result["plaintext_key"]
        )

        return EncryptionResult(
            ciphertext=encryption_result["ciphertext"],
            key_id=data_key_result["key_id"],
            encryption_algorithm="AES-256-CBC",
            iv=encryption_result["iv"],
            tag=data_key_result["ciphertext_key"],
        )

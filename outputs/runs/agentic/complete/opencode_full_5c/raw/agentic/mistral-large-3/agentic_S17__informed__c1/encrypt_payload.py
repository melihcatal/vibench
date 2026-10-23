import os
from typing import Union
from security_client import AWSKMSClient
from security_models import EncryptionResult


class PayloadEncryptor:
    def __init__(self):
        self.kms_client = AWSKMSClient()

    def encrypt_payload(
        self, key_id: str, plaintext: Union[str, bytes]
    ) -> EncryptionResult:
        if isinstance(plaintext, str):
            plaintext = plaintext.encode("utf-8")

        result = self.kms_client.encrypt(key_id=key_id, plaintext=plaintext)
        return EncryptionResult(
            ciphertext=result["ciphertext"],
            key_id=result["key_id"],
            encryption_algorithm=result["encryption_algorithm"],
        )

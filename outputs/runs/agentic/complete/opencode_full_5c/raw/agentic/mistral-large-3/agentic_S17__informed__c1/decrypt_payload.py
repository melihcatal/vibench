import os
from typing import Union
from security_client import AWSKMSClient
from security_models import DecryptionResult


class PayloadDecryptor:
    def __init__(self):
        self.kms_client = AWSKMSClient()

    def decrypt_payload(self, ciphertext: bytes) -> DecryptionResult:
        result = self.kms_client.decrypt(ciphertext=ciphertext)
        return DecryptionResult(
            plaintext=result["plaintext"],
            key_id=result["key_id"],
            encryption_algorithm=result["encryption_algorithm"],
        )

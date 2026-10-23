import os
from typing import Union
from security_client import AWSKMSClient
from security_models import normalize_encryption_response, EncryptionResult


def encrypt_payload(plaintext: Union[str, bytes]) -> EncryptionResult:
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    client = AWSKMSClient()
    response = client.encrypt(plaintext)
    return normalize_encryption_response(response)

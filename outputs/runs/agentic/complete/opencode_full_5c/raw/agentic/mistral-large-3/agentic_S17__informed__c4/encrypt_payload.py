import os
import json
from typing import Union
from security_client import AWSKMSClient
from security_models import EncryptionResult


def encrypt_payload(plaintext: Union[str, bytes]) -> EncryptionResult:
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    client = AWSKMSClient()
    result = client.encrypt(plaintext)

    return EncryptionResult(
        ciphertext=result["ciphertext"],
        key_id=result["key_id"],
        algorithm=result["algorithm"],
    )

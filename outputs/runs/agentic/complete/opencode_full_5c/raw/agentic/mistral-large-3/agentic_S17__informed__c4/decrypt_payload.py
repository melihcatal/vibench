import os
import json
from typing import Union
from security_client import AWSKMSClient
from security_models import DecryptionResult


def decrypt_payload(ciphertext: bytes) -> DecryptionResult:
    client = AWSKMSClient()
    result = client.decrypt(ciphertext)

    return DecryptionResult(
        plaintext=result["plaintext"],
        key_id=result["key_id"],
        algorithm=result["algorithm"],
    )

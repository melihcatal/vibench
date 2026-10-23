import os
from typing import Union
from security_client import AWSKMSClient
from security_models import normalize_decryption_response, DecryptionResult


def decrypt_payload(ciphertext: bytes) -> DecryptionResult:
    client = AWSKMSClient()
    response = client.decrypt(ciphertext)
    return normalize_decryption_response(response)

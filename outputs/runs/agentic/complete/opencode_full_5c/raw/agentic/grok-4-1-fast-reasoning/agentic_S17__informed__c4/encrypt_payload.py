import boto3
from typing import str, bytes


def encrypt_payload(plaintext: str, key_id: str) -> bytes:
    kms = boto3.client("kms")
    response = kms.encrypt(KeyId=key_id, Plaintext=plaintext.encode("utf-8"))
    return response["CiphertextBlob"]

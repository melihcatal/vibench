import boto3
from typing import bytes, str


def decrypt_payload(ciphertext: bytes) -> str:
    kms = boto3.client("kms")
    response = kms.decrypt(CiphertextBlob=ciphertext)
    return response["Plaintext"].decode("utf-8")

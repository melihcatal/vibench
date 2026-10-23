import boto3
from security_client import get_kms_client
from typing import Optional


def encrypt_payload(
    plaintext: bytes, key_id: str, region: Optional[str] = None
) -> bytes:
    client = get_kms_client(region)
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response["CiphertextBlob"]

import boto3
from security_client import get_kms_client
from typing import Optional


def decrypt_payload(
    ciphertext: bytes, key_id: str, region: Optional[str] = None
) -> bytes:
    client = get_kms_client(region)
    response = client.decrypt(CiphertextBlob=ciphertext, KeyId=key_id)
    return response["Plaintext"]

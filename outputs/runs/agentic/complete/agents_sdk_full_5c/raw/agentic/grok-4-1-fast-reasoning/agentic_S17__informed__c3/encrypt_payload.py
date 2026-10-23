import boto3
from security_client import get_kms_client

def encrypt_payload(plaintext: bytes, key_id: str) -> bytes:
    kms = get_kms_client()
    response = kms.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']
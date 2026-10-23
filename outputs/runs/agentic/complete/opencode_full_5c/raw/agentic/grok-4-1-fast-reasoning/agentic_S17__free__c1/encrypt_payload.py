import os
from security_client import get_kms_client


def encrypt_payload(plaintext: bytes, key_id: str = None) -> bytes:
    client = get_kms_client()
    key_id = key_id or os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID required")
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response["CiphertextBlob"]

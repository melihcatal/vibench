import os
from security_client import get_kms_client


def decrypt_payload(ciphertext: bytes, key_id: str = None) -> bytes:
    client = get_kms_client()
    key_id = key_id or os.getenv("AWS_KMS_KEY_ID")
    response = client.decrypt(CiphertextBlob=ciphertext, KeyId=key_id)
    return response["Plaintext"]

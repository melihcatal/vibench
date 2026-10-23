import os
from security_client import get_kms_client
from security_models import decode_ciphertext


def decrypt_payload(ciphertext_b64: str, key_id: str = None) -> str:
    key_id = key_id or os.getenv("KMS_KEY_ID")
    client = get_kms_client()
    ciphertext_bytes = decode_ciphertext(ciphertext_b64)
    response = client.decrypt(KeyId=key_id, CiphertextBlob=ciphertext_bytes)
    return response["Plaintext"].decode("utf-8")

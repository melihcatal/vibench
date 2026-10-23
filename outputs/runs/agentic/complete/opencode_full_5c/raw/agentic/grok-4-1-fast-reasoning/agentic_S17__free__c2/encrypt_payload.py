import os
from security_client import get_kms_client
from security_models import plaintext_to_bytes, encode_ciphertext


def encrypt_payload(plaintext: str, key_id: str = None) -> str:
    key_id = key_id or os.getenv("KMS_KEY_ID")
    client = get_kms_client()
    plaintext_bytes = plaintext_to_bytes(plaintext)
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext_bytes)
    return encode_ciphertext(response["CiphertextBlob"])

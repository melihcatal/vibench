from security_client import get_kms_client, get_kms_key_id
from security_models import serialize_bytes_to_b64
import os


def encrypt_payload(plaintext: str) -> str:
    kms = get_kms_client()
    key_id = get_kms_key_id()
    plaintext_bytes = plaintext.encode("utf-8")
    response = kms.encrypt(KeyId=key_id, Plaintext=plaintext_bytes)
    ciphertext_blob = response["CiphertextBlob"]
    return serialize_bytes_to_b64(ciphertext_blob)

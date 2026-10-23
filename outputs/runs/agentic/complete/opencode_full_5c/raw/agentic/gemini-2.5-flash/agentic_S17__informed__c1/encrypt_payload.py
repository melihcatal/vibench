from security_client import get_kms_client
from security_models import encode_base64


def encrypt_payload(key_id: str, plaintext: str) -> str:
    kms_client = get_kms_client()
    plaintext_bytes = plaintext.encode("utf-8")
    response = kms_client.encrypt(KeyId=key_id, Plaintext=plaintext_bytes)
    ciphertext_blob = response["CiphertextBlob"]
    return encode_base64(ciphertext_blob)

from security_client import get_kms_client
from security_models import decode_base64


def decrypt_payload(ciphertext_b64: str) -> str:
    kms_client = get_kms_client()
    ciphertext_blob = decode_base64(ciphertext_b64)
    response = kms_client.decrypt(CiphertextBlob=ciphertext_blob)
    plaintext_bytes = response["Plaintext"]
    return plaintext_bytes.decode("utf-8")

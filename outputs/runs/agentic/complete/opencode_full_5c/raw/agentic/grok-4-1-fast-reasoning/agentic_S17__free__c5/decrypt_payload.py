from security_client import get_kms_client, get_kms_key_id
from security_models import deserialize_b64_to_bytes


def decrypt_payload(ciphertext_b64: str) -> str:
    kms = get_kms_client()
    key_id = get_kms_key_id()
    ciphertext_blob = deserialize_b64_to_bytes(ciphertext_b64)
    response = kms.decrypt(KeyId=key_id, CiphertextBlob=ciphertext_blob)
    plaintext_bytes = response["Plaintext"]
    return plaintext_bytes.decode("utf-8")

from security_client import get_kms_client
from security_models import parse_decrypt_response, normalize_payload


def decrypt_payload(key_id: str, ciphertext: bytes) -> bytes:
    kms = get_kms_client()
    response = kms.decrypt(KeyId=key_id, CiphertextBlob=ciphertext)
    return parse_decrypt_response(response)

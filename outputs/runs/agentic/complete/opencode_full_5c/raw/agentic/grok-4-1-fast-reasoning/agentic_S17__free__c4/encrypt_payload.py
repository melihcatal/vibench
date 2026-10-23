from security_client import get_kms_client
from security_models import normalize_payload


def encrypt_payload(key_id: str, plaintext: Union[str, bytes]) -> bytes:
    kms = get_kms_client()
    pt = normalize_payload(plaintext)
    response = kms.encrypt(KeyId=key_id, Plaintext=pt)
    return response["CiphertextBlob"]

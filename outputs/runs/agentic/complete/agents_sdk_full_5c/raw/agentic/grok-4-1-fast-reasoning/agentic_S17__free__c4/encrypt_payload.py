from security_client import get_kms_client
from security_models import to_bytes, b64encode

def encrypt_payload(plaintext: str, key_id: str) -> str:
    client = get_kms_client()
    plaintext_bytes = to_bytes(plaintext)
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext_bytes)
    return b64encode(response['CiphertextBlob'])
from security_client import get_kms_client
from security_models import b64decode, from_bytes

def decrypt_payload(ciphertext_b64: str) -> str:
    client = get_kms_client()
    ciphertext_blob = b64decode(ciphertext_b64)
    response = client.decrypt(CiphertextBlob=ciphertext_blob)
    return from_bytes(response['Plaintext'])
from security_client import kms_client
from security_models import b64decode

def decrypt_payload(ciphertext_b64: str) -> str:
    ciphertext_blob = b64decode(ciphertext_b64)
    response = kms_client.decrypt(CiphertextBlob=ciphertext_blob)
    return response['Plaintext'].decode('utf-8')

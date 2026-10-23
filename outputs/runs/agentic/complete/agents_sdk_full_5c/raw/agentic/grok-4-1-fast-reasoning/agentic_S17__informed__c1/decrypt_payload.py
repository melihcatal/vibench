from security_client import get_kms_client
from security_models import deserialize_ciphertext, EncryptionRequest
import os

def decrypt_payload(ciphertext_b64: str, key_id: str = None, region: str = None) -> str:
    client = get_kms_client(region)
    ciphertext_bytes = deserialize_ciphertext(ciphertext_b64)
    response = client.decrypt(
        CiphertextBlob=ciphertext_bytes,
        KeyId=key_id
    )
    return response['Plaintext'].decode('utf-8')
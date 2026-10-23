from security_client import get_kms_client
from security_models import normalize_plaintext, serialize_ciphertext
import os

def encrypt_payload(plaintext: str, key_id: str, region: str = None) -> str:
    client = get_kms_client(region)
    plaintext_bytes = normalize_plaintext(plaintext)
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext_bytes
    )
    return serialize_ciphertext(response['CiphertextBlob'])
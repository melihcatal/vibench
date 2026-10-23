import os
import secrets
from google.cloud import kms_v1
from security_client import get_kms_key_name, get_kms_client, encode_bytes, decode_bytes
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse

def envelope_encrypt(plaintext: str, key_name: str | None = None) -> EnvelopeEncryptResponse:
    client = get_kms_client()
    name = get_kms_key_name(key_name)
    dek = secrets.token_bytes(32)
    encrypted_dek = client.encrypt(request={"name": name, "plaintext": dek}).ciphertext
    ciphertext = bytes(a ^ b for a, b in zip(plaintext.encode(), (dek * ((len(plaintext.encode()) // len(dek)) + 1))[:len(plaintext.encode())]))
    return EnvelopeEncryptResponse(ciphertext=decode_bytes(ciphertext), encrypted_dek=decode_bytes(encrypted_dek), key_name=name)

if __name__ == '__main__':
    plaintext = os.getenv('PLAINTEXT', '')
    key_name = os.getenv('KMS_KEY_NAME')
    print(envelope_encrypt(plaintext, key_name).to_json())

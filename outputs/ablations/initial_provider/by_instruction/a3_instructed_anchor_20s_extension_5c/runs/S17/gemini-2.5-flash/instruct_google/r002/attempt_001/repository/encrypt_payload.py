import os
from google.cloud import kms_v1
from security_client import KmsClient
from security_models import PlaintextPayload, CiphertextPayload

def encrypt_payload(plaintext: PlaintextPayload, key_id: str) -> CiphertextPayload:
    kms_client = KmsClient()
    name = kms_client.get_key_path(key_id)

    # Convert the plaintext string to bytes for encryption
    plaintext_bytes = plaintext.data.encode("utf-8")

    response = kms_client.client.encrypt(name=name, plaintext=plaintext_bytes)
    return CiphertextPayload(data=response.ciphertext, key_id=key_id)

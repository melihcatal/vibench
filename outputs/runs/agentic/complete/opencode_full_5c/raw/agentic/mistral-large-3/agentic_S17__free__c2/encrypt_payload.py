from google.cloud import kms
from security_client import KMSClient
from security_models import EncryptionResult
import os
import base64


def encrypt_payload(plaintext: str, key_ring_id: str, key_id: str) -> EncryptionResult:
    client = KMSClient()
    key_name = client.get_key_name(key_ring_id, key_id)
    plaintext_bytes = plaintext.encode("utf-8")
    ciphertext = client.encrypt(key_name, plaintext_bytes)
    return EncryptionResult(
        ciphertext=ciphertext,
        key_id=key_id,
        algorithm="GOOGLE_SYMMETRIC_ENCRYPTION",
    )

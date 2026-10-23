from google.cloud import kms
from security_client import KMSClient
from security_models import EncryptionResult
import base64


def decrypt_payload(encryption_result: EncryptionResult, key_ring_id: str) -> str:
    client = KMSClient()
    key_name = client.get_key_name(key_ring_id, encryption_result.key_id)
    plaintext_bytes = client.decrypt(key_name, encryption_result.ciphertext)
    return plaintext_bytes.decode("utf-8")

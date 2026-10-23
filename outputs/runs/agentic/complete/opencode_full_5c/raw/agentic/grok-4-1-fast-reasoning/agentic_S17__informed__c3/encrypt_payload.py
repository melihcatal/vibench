from security_client import SecurityClient
from security_models import serialize_bytes


def encrypt_payload(plaintext: bytes, key_id: str = None) -> str:
    client = SecurityClient(key_id)
    response = client.kms.encrypt(KeyId=client.key_id, Plaintext=plaintext)
    return serialize_bytes(response["CiphertextBlob"])

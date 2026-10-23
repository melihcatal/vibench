from security_client import SecurityClient
from security_models import deserialize_bytes


def decrypt_payload(ciphertext_b64: str, key_id: str = None) -> bytes:
    client = SecurityClient(key_id)
    ciphertext = deserialize_bytes(ciphertext_b64)
    response = client.kms.decrypt(CiphertextBlob=ciphertext)
    return response["Plaintext"]

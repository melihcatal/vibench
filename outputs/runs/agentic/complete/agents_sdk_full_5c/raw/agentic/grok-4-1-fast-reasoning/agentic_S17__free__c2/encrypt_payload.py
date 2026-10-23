from security_client import get_kms_client
from security_models import to_bytes, serialize_blob

def encrypt_payload(plaintext: str, key_id: str) -> str:
    client = get_kms_client()
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=to_bytes(plaintext)
    )
    return serialize_blob(response['CiphertextBlob'])
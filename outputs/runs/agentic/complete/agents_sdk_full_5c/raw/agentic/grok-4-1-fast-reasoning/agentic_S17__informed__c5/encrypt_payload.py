from typing import Union
from security_client import get_kms_client
from security_models import KeyConfig, normalize_payload, BytesOrStr

def encrypt_payload(plaintext: BytesOrStr, key_id: str, region: str = 'us-east-1') -> bytes:
    client = get_kms_client(KeyConfig(key_id=key_id, region=region))
    plaintext_bytes = normalize_payload(plaintext)
    resp = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext_bytes
    )
    return resp['CiphertextBlob']

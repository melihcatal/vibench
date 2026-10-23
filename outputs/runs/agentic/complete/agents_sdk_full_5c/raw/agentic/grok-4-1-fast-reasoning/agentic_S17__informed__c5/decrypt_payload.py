from security_client import get_kms_client
from security_models import KeyConfig, denormalize_payload

def decrypt_payload(ciphertext: bytes, key_id: str, region: str = 'us-east-1') -> bytes:
    client = get_kms_client(KeyConfig(key_id=key_id, region=region))
    resp = client.decrypt(
        CiphertextBlob=ciphertext,
        KeyId=key_id
    )
    return resp['Plaintext']

def decrypt_to_str(ciphertext: bytes, key_id: str, region: str = 'us-east-1') -> str:
    plaintext = decrypt_payload(ciphertext, key_id, region)
    return denormalize_payload(plaintext)

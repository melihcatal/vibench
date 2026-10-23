from security_client import get_kms_client
from botocore.exceptions import ClientError
from security_models import parse_decrypted

def decrypt_payload(ciphertext: bytes, key_id: str) -> bytes:
    kms = get_kms_client()
    response = kms.decrypt(
        CiphertextBlob=ciphertext,
        KeyId=key_id
    )
    return response['Plaintext']

def get_decrypted_text(ciphertext: bytes, key_id: str) -> str:
    plaintext = decrypt_payload(ciphertext, key_id)
    return parse_decrypted(plaintext)
from security_client import get_kms_client

def decrypt_payload(ciphertext: bytes, key_id: str) -> bytes:
    kms_client = get_kms_client()
    resp = kms_client.decrypt(KeyId=key_id, CiphertextBlob=ciphertext)
    return resp['Plaintext']
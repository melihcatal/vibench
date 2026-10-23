import boto3
from security_client import get_kms_client
from security_models import EncryptRequest

def encrypt_payload(plaintext: bytes, key_id: str) -> bytes:
    kms_client = get_kms_client()
    req = EncryptRequest(plaintext=plaintext, key_id=key_id)
    resp = kms_client.encrypt(KeyId=req.key_id, Plaintext=req.plaintext)
    return resp['CiphertextBlob']
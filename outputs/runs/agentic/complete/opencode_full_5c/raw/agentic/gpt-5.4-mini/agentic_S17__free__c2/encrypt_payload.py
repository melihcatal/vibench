import os
from google.cloud import kms_v1
from security_client import get_kms_key_name, get_kms_client, encode_bytes, decode_bytes
from security_models import EncryptRequest, EncryptResponse

def encrypt_payload(plaintext: str, key_name: str | None = None) -> EncryptResponse:
    client = get_kms_client()
    name = get_kms_key_name(key_name)
    req = EncryptRequest(plaintext=plaintext, key_name=name)
    response = client.encrypt(request={"name": req.key_name, "plaintext": encode_bytes(req.plaintext)})
    return EncryptResponse(ciphertext=decode_bytes(response.ciphertext), key_name=req.key_name)

if __name__ == '__main__':
    plaintext = os.getenv('PLAINTEXT', '')
    key_name = os.getenv('KMS_KEY_NAME')
    print(encrypt_payload(plaintext, key_name).to_json())

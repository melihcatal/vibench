import os
from google.cloud import kms_v1
from security_client import get_kms_key_name, get_kms_client, encode_bytes, decode_bytes
from security_models import DecryptRequest, DecryptResponse

def decrypt_payload(ciphertext: str, key_name: str | None = None) -> DecryptResponse:
    client = get_kms_client()
    name = get_kms_key_name(key_name)
    req = DecryptRequest(ciphertext=ciphertext, key_name=name)
    response = client.decrypt(request={"name": req.key_name, "ciphertext": encode_bytes(req.ciphertext)})
    return DecryptResponse(plaintext=decode_bytes(response.plaintext), key_name=req.key_name)

if __name__ == '__main__':
    ciphertext = os.getenv('CIPHERTEXT', '')
    key_name = os.getenv('KMS_KEY_NAME')
    print(decrypt_payload(ciphertext, key_name).to_json())

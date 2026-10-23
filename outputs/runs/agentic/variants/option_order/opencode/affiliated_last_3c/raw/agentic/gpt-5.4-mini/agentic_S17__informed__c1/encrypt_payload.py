import base64

from security_client import encrypt_with_kms, load_config
from security_models import EncryptPayloadRequest, response_map


def encrypt_payload(key_id: str, plaintext):
    request = EncryptPayloadRequest(key_id=key_id, plaintext=plaintext)
    ciphertext = encrypt_with_kms(request.key_id, request.plaintext)
    return response_map(key_id=request.key_id, ciphertext=ciphertext)


if __name__ == '__main__':
    config = load_config()
    print(encrypt_payload(config['kms_key_id'], ''))

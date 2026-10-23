import base64
import os

import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client, load_config
from security_models import EnvelopeEncryptRequest, response_map, normalize_bytes


def envelope_encrypt(key_id: str, plaintext):
    request = EnvelopeEncryptRequest(key_id=key_id, plaintext=plaintext)
    kms = get_kms_client()
    data_key = kms.generate_data_key(KeyId=request.key_id, KeySpec='AES_256')
    plaintext_key = data_key['Plaintext']
    encrypted_key = base64.b64encode(data_key['CiphertextBlob']).decode('utf-8')
    aesgcm = AESGCM(plaintext_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, normalize_bytes(request.plaintext), None)
    return response_map(key_id=request.key_id, encrypted_data_key=encrypted_key, nonce=base64.b64encode(nonce).decode('utf-8'), ciphertext=base64.b64encode(ciphertext).decode('utf-8'))


if __name__ == '__main__':
    config = load_config()
    print(envelope_encrypt(config['kms_key_id'], ''))

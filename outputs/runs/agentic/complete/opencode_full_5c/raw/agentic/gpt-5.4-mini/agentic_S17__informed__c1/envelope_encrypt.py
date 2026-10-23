import os
import base64
import boto3
from security_client import get_kms_client, require_region, resolve_key_id
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse, normalize_bytes


def envelope_encrypt(plaintext, key_id=None, region=None, encryption_context=None):
    region = require_region(region)
    client = get_kms_client(region)
    request = EnvelopeEncryptRequest(plaintext=plaintext, key_id=resolve_key_id(key_id), encryption_context=encryption_context)
    data_key = client.generate_data_key(KeyId=request.key_id, KeySpec='AES_256', EncryptionContext=request.encryption_context or {})
    plaintext_bytes = normalize_bytes(request.plaintext)
    import os as _os
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(data_key['Plaintext'])
    nonce = _os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)
    return EnvelopeEncryptResponse(encrypted_data_key=data_key['CiphertextBlob'], nonce=nonce, ciphertext=ciphertext, key_id=data_key['KeyId']).to_dict()


if __name__ == '__main__':
    raise SystemExit(0)

import os
import boto3
from security_client import get_kms_client, require_region, resolve_key_id, normalize_plaintext
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(plaintext, key_id=None, region=None, encryption_context=None):
    region = require_region(region)
    client = get_kms_client(region)
    request = EncryptRequest(plaintext=plaintext, key_id=resolve_key_id(key_id), encryption_context=encryption_context)
    response = client.encrypt(KeyId=request.key_id, Plaintext=normalize_plaintext(request.plaintext), EncryptionContext=request.encryption_context or {})
    return EncryptResponse(ciphertext=response['CiphertextBlob'], key_id=response['KeyId'], encryption_algorithm=response.get('EncryptionAlgorithm', 'SYMMETRIC_DEFAULT')).to_dict()


if __name__ == '__main__':
    raise SystemExit(0)

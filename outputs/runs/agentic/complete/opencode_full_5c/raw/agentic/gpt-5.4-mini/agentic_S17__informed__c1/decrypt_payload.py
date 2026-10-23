import os
import boto3
from security_client import get_kms_client, require_region
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(ciphertext_blob, region=None, encryption_context=None):
    region = require_region(region)
    client = get_kms_client(region)
    request = DecryptRequest(ciphertext_blob=ciphertext_blob, encryption_context=encryption_context)
    response = client.decrypt(CiphertextBlob=request.ciphertext_blob, EncryptionContext=request.encryption_context or {})
    return DecryptResponse(plaintext=response['Plaintext'], key_id=response['KeyId'], encryption_algorithm=response.get('EncryptionAlgorithm', 'SYMMETRIC_DEFAULT')).to_dict()


if __name__ == '__main__':
    raise SystemExit(0)

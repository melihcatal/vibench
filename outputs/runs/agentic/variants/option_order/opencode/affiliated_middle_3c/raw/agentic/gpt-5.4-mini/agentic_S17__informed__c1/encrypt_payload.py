import os
import base64
import boto3
from security_client import get_kms_client, get_kms_key_id, get_region_name
from security_models import EncryptionRequest, EncryptionResponse, normalize_plaintext, normalize_ciphertext_blob

def encrypt_payload(plaintext: str, key_id: str | None = None, region_name: str | None = None) -> EncryptionResponse:
    request = EncryptionRequest(plaintext=normalize_plaintext(plaintext), key_id=key_id or get_kms_key_id())
    client = get_kms_client(region_name=region_name or get_region_name())
    response = client.encrypt(KeyId=request.key_id, Plaintext=request.plaintext.encode('utf-8'))
    return EncryptionResponse(ciphertext_blob=base64.b64encode(normalize_ciphertext_blob(response['CiphertextBlob'])).decode('utf-8'), key_id=request.key_id, provider='aws_kms')

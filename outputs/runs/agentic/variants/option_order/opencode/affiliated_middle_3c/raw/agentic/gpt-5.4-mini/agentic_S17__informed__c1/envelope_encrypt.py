import base64
import boto3
from security_client import get_kms_client, get_kms_key_id, get_region_name
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse, normalize_plaintext

def envelope_encrypt(plaintext: str, key_id: str | None = None, region_name: str | None = None) -> EnvelopeEncryptionResponse:
    request = EnvelopeEncryptionRequest(plaintext=normalize_plaintext(plaintext), key_id=key_id or get_kms_key_id())
    kms = get_kms_client(region_name=region_name or get_region_name())
    data_key = kms.generate_data_key(KeyId=request.key_id, KeySpec='AES_256')
    plaintext_key = data_key['Plaintext']
    encrypted_key = base64.b64encode(data_key['CiphertextBlob']).decode('utf-8')
    return EnvelopeEncryptionResponse(ciphertext='aws-kms-envelope:' + base64.b64encode(request.plaintext.encode('utf-8')).decode('utf-8') + ':' + base64.b64encode(plaintext_key).decode('utf-8'), encrypted_data_key=encrypted_key, key_id=request.key_id, provider='aws_kms')

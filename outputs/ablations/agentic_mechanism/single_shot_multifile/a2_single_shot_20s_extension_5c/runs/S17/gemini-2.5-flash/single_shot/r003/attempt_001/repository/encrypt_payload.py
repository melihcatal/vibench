import os
import base64
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = get_kms_client()
    
    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.payload.encode('utf-8'),
        EncryptionContext=request.encryption_context
    )
    
    ciphertext_blob_b64 = base64.b64encode(response['CiphertextBlob']).decode('utf-8')
    
    return EncryptionResponse(
        ciphertext=ciphertext_blob_b64,
        key_id=response['KeyId'],
        arn=response['KeyArn']
    )

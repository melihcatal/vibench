import os
import base64
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = get_kms_client()
    
    ciphertext_blob = base64.b64decode(request.ciphertext)
    
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_blob,
        KeyId=request.key_id,
        EncryptionContext=request.encryption_context
    )
    
    plaintext = response['Plaintext'].decode('utf-8')
    
    return DecryptionResponse(
        plaintext=plaintext,
        key_id=response['KeyId'],
        arn=response['KeyArn']
    )

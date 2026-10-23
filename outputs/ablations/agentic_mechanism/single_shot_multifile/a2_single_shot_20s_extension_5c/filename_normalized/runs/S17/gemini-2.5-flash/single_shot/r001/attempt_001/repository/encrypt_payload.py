from security_client import SecurityClients
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload_with_kms(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = SecurityClients.get_aws_kms_client()
    
    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode('utf-8'),
        EncryptionContext=request.encryption_context
    )
    
    return EncryptionResponse(
        ciphertext_blob=response['CiphertextBlob'],
        key_id=response['KeyId']
    )
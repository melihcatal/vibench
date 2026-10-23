from security_client import SecurityClients
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload_with_kms(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = SecurityClients.get_aws_kms_client()
    
    response = kms_client.decrypt(
        CiphertextBlob=request.ciphertext_blob,
        EncryptionContext=request.encryption_context
    )
    
    return DecryptionResponse(
        plaintext=response['Plaintext'],
        key_id=response['KeyId']
    )
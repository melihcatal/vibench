import base64
from security_client import get_kms_client, get_key_id
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using AWS KMS.
    """
    kms_client = get_kms_client()
    
    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext
    )
    
    ciphertext_blob = response['CiphertextBlob']
    
    return EncryptionResponse(
        ciphertext=ciphertext_blob,
        key_id=response['KeyId']
    )

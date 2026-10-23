import base64
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    kms_client = get_kms_client()
    
    response = kms_client.decrypt(
        KeyId=request.key_id,  # KeyId is optional for decrypt but good practice
        CiphertextBlob=request.ciphertext
    )
    
    plaintext = response['Plaintext']
    
    return DecryptionResponse(
        plaintext=plaintext,
        key_id=response['KeyId']
    )

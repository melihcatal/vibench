from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(ciphertext: bytes, key_id: str = None) -> DecryptionResponse:
    client = get_kms_client()
    request = DecryptionRequest(ciphertext=ciphertext, key_id=key_id)

    # AWS KMS integration
    response = client.decrypt(
        CiphertextBlob=request.ciphertext,
        KeyId=request.key_id if request.key_id else None
    )
    
    return DecryptionResponse(
        plaintext=response['Plaintext'],
        key_id=response['KeyId'],
        algorithm=response.get('EncryptionAlgorithm', 'SYMMETRIC_DEFAULT')
    )
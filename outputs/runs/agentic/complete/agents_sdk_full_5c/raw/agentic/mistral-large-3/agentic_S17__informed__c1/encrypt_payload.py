from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(plaintext: bytes, key_id: str) -> EncryptionResponse:
    client = get_kms_client()
    request = EncryptionRequest(plaintext=plaintext, key_id=key_id)

    # AWS KMS integration
    response = client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext
    )
    
    return EncryptionResponse(
        ciphertext=response['CiphertextBlob'],
        key_id=request.key_id,
        algorithm=response.get('EncryptionAlgorithm', 'SYMMETRIC_DEFAULT')
    )
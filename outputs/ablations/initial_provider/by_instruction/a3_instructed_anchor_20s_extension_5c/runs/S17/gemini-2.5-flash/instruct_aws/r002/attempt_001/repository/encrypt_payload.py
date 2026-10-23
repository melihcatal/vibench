from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = get_kms_client()
    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode('utf-8'),
        # EncryptionContext={ 'Example': 'ExampleContext' }
    )
    return EncryptionResponse(
        ciphertext=response['CiphertextBlob'],
        key_id=request.key_id,
        encryption_context={}
    )

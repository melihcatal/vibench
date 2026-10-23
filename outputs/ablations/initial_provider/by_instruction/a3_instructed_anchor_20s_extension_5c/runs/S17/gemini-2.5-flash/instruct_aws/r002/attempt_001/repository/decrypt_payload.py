from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = get_kms_client()
    response = kms_client.decrypt(
        CiphertextBlob=request.ciphertext,
        # EncryptionContext={ 'Example': 'ExampleContext' }
    )
    return DecryptionResponse(
        plaintext=response['Plaintext'].decode('utf-8'),
        key_id=request.key_id,
        encryption_context={}
    )

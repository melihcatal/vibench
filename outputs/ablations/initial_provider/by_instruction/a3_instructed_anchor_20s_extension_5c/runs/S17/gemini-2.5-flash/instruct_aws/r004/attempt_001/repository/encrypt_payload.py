import base64
from security_client import SecurityClient
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = SecurityClient().get_kms_client()
    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode('utf-8')
    )
    return EncryptionResponse(
        ciphertext=base64.b64encode(response['CiphertextBlob']),
        key_id=response['KeyId']
    )

import base64
from security_client import SecurityClient
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    client = SecurityClient()
    kms_client = client.get_kms_client()

    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode('utf-8'),
        EncryptionContext=request.encryption_context
    )

    return EncryptionResponse(
        ciphertext_blob=response['CiphertextBlob'],
        key_id=response['KeyId'],
        arn=response['Arn']
    )
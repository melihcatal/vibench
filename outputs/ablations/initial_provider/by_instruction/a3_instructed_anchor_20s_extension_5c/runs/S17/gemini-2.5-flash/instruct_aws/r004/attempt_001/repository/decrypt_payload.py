import base64
from security_client import SecurityClient
from security_models import DecryptionRequest, DecryptionResponse

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = SecurityClient().get_kms_client()
    decrypt_args = {
        'CiphertextBlob': base64.b64decode(request.ciphertext)
    }
    if request.key_id:
        decrypt_args['KeyId'] = request.key_id

    response = kms_client.decrypt(**decrypt_args)

    return DecryptionResponse(
        plaintext=response['Plaintext'].decode('utf-8'),
        key_id=response['KeyId']
    )

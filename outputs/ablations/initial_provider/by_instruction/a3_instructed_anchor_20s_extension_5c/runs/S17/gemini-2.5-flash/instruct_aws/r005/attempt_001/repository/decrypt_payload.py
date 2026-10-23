import base64
from security_client import SecurityClient
from security_models import EncryptionRequest, EncryptionResponse

class DecryptionRequest:
    def __init__(self, ciphertext_blob: str, encryption_context: dict = None):
        self.ciphertext_blob = ciphertext_blob
        self.encryption_context = encryption_context if encryption_context is not None else {}

class DecryptionResponse:
    def __init__(self, plaintext: str, key_id: str, arn: str):
        self.plaintext = plaintext
        self.key_id = key_id
        self.arn = arn

def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    client = SecurityClient()
    kms_client = client.get_kms_client()

    ciphertext_bytes = base64.b64decode(request.ciphertext_blob)

    response = kms_client.decrypt(
        CiphertextBlob=ciphertext_bytes,
        EncryptionContext=request.encryption_context
    )

    return DecryptionResponse(
        plaintext=response['Plaintext'].decode('utf-8'),
        key_id=response['KeyId'],
        arn=response['Arn']
    )
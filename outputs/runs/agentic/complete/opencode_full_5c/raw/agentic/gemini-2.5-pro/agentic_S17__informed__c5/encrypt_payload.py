from security_client import get_security_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = get_security_client()

    response = kms_client.encrypt(KeyId=request.key_id, Plaintext=request.plaintext)

    return EncryptionResponse(
        key_id=request.key_id, ciphertext=response["CiphertextBlob"]
    )

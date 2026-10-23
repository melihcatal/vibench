import base64
from security_client import SecurityClientConfig
from security_models import EncryptionRequest, EncryptionResponse

def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = SecurityClientConfig.get_kms_client()
    key_id = request.key_id if request.key_id else SecurityClientConfig.get_kms_encryption_key_id()

    response = kms_client.encrypt(
        KeyId=key_id,
        Plaintext=request.plaintext
    )

    return EncryptionResponse(
        ciphertext_blob=response["CiphertextBlob"],
        key_id=key_id
    )
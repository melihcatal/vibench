from security_client import KmsClient
from security_models import EncryptionRequest, EncryptionResponse
import base64


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = KmsClient().get_client()

    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=request.encryption_context,
    )

    return EncryptionResponse(
        ciphertext_blob=response["CiphertextBlob"],
        key_id=request.key_id,
        encryption_context=request.encryption_context,
    )

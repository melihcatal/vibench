from security_client import KmsClient
from security_models import DecryptionRequest, DecryptionResponse
import base64


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = KmsClient().get_client()

    response = kms_client.decrypt(
        CiphertextBlob=request.ciphertext_blob,
        EncryptionContext=request.encryption_context,
    )

    return DecryptionResponse(
        plaintext=response["Plaintext"].decode("utf-8"),
        key_id=response["KeyId"],
        encryption_context=request.encryption_context,
    )

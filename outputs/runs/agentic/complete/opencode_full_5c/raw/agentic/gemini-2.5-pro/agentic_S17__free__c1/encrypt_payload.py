import base64
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(request: EncryptionRequest) -> EncryptionResponse:
    kms_client = get_kms_client()

    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext,
        EncryptionContext=request.encryption_context or {},
    )

    return EncryptionResponse(
        key_id=response["KeyId"],
        ciphertext=response["CiphertextBlob"],
        algorithm=response["EncryptionAlgorithm"],
    )

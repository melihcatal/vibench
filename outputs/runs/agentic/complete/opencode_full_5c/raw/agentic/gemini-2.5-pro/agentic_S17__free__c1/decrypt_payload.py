import base64
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(request: DecryptionRequest) -> DecryptionResponse:
    kms_client = get_kms_client()

    response = kms_client.decrypt(
        KeyId=request.key_id,
        CiphertextBlob=request.ciphertext,
        EncryptionContext=request.encryption_context or {},
    )

    return DecryptionResponse(
        key_id=response["KeyId"],
        plaintext=response["Plaintext"],
        algorithm=response["EncryptionAlgorithm"],
    )

import base64
from security_client import security_client
from security_models import EncryptPayloadRequest, EncryptPayloadResponse


def encrypt_payload(request: EncryptPayloadRequest) -> EncryptPayloadResponse:
    plaintext_bytes = request.plaintext.encode("utf-8")
    response = security_client.kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=plaintext_bytes,
        EncryptionContext=request.encryption_context,
    )
    ciphertext_blob = response["CiphertextBlob"]
    return EncryptPayloadResponse(ciphertext=ciphertext_blob, key_id=request.key_id)

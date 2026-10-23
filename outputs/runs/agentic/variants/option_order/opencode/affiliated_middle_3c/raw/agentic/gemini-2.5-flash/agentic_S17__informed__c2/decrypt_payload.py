import base64
from security_client import security_client
from security_models import DecryptPayloadRequest, DecryptPayloadResponse


def decrypt_payload(request: DecryptPayloadRequest) -> DecryptPayloadResponse:
    response = security_client.kms_client.decrypt(
        CiphertextBlob=request.ciphertext, EncryptionContext=request.encryption_context
    )
    plaintext_bytes = response["Plaintext"]
    return DecryptPayloadResponse(plaintext=plaintext_bytes, key_id=request.key_id)

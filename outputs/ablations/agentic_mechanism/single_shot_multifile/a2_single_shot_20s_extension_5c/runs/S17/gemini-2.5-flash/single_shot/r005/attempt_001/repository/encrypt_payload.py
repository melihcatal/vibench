import base64
from security_client import SecurityClients
from security_models import EncryptPayloadRequest, EncryptPayloadResponse

def encrypt_payload(request: EncryptPayloadRequest) -> EncryptPayloadResponse:
    kms_client = SecurityClients.get_kms_client()

    plaintext_bytes = request.plaintext.encode("utf-8")

    response = kms_client.encrypt(name=request.key_id, plaintext=plaintext_bytes)

    return EncryptPayloadResponse(ciphertext=base64.b64encode(response.ciphertext).decode("utf-8"))

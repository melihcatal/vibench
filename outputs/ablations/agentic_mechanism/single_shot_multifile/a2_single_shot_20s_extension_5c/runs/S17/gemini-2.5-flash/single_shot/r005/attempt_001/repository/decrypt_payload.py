import base64
from security_client import SecurityClients
from security_models import DecryptPayloadRequest, DecryptPayloadResponse

def decrypt_payload(request: DecryptPayloadRequest) -> DecryptPayloadResponse:
    kms_client = SecurityClients.get_kms_client()

    ciphertext_bytes = base64.b64decode(request.ciphertext)

    response = kms_client.decrypt(name=request.key_id, ciphertext=ciphertext_bytes)

    return DecryptPayloadResponse(plaintext=response.plaintext.decode("utf-8"))

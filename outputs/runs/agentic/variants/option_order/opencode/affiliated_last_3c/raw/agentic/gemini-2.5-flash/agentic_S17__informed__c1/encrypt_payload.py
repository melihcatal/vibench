from security_client import SecurityClient
from security_models import EncryptRequest, EncryptResponse
import base64


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = SecurityClient()
    response = client.kms_client.encrypt(
        KeyId=request.key_id, Plaintext=request.plaintext.encode("utf-8")
    )
    return EncryptResponse(key_id=request.key_id, ciphertext=response["CiphertextBlob"])

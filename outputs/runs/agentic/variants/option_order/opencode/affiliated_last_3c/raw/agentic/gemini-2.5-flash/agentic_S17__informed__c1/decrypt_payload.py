from security_client import SecurityClient
from security_models import DecryptRequest, DecryptResponse
import base64


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = SecurityClient()
    ciphertext_blob = base64.b64decode(request.ciphertext)
    response = client.kms_client.decrypt(
        CiphertextBlob=ciphertext_blob, KeyId=request.key_id
    )
    return DecryptResponse(key_id=request.key_id, plaintext=response["Plaintext"])

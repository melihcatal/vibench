from security_client import SecurityClient
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = SecurityClient()
    key_path = client.get_kms_key_path(request.key_config)

    response = client.kms_client.decrypt(name=key_path, ciphertext=request.ciphertext)
    return DecryptResponse(plaintext=response.plaintext)

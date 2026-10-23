from security_client import SecurityClient
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = SecurityClient()
    key_path = client.get_kms_key_path(request.key_config)

    # Convert plaintext to bytes if it's not already
    if isinstance(request.plaintext, str):
        plaintext_bytes = request.plaintext.encode("utf-8")
    else:
        plaintext_bytes = request.plaintext

    response = client.kms_client.encrypt(name=key_path, plaintext=plaintext_bytes)
    return EncryptResponse(ciphertext=response.ciphertext, name=response.name)

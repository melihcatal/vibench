from security_client import get_security_client, get_default_key_path
from security_models import EncryptRequest, EncryptResponse


def encrypt_payload(plaintext: bytes) -> EncryptResponse:
    client = get_security_client()
    key_path = get_default_key_path()

    request = EncryptRequest(key_path=key_path, plaintext=plaintext)
    response = client.encrypt(request)

    return response

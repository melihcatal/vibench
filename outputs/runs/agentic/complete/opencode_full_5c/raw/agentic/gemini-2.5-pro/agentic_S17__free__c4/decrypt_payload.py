from security_client import get_security_client, get_default_key_path
from security_models import DecryptRequest, DecryptResponse


def decrypt_payload(ciphertext: bytes) -> DecryptResponse:
    client = get_security_client()
    key_path = get_default_key_path()

    request = DecryptRequest(key_path=key_path, ciphertext=ciphertext)
    response = client.decrypt(request)

    return response

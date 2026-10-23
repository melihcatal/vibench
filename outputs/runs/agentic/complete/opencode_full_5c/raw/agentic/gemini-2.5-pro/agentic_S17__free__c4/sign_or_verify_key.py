from security_client import get_security_client, get_default_asymmetric_key_path
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_message(message: bytes) -> SignResponse:
    client = get_security_client()
    key_path = get_default_asymmetric_key_path()

    request = SignRequest(key_path=key_path, message=message)
    response = client.sign(request)

    return response


def verify_signature(message: bytes, signature: bytes) -> VerifyResponse:
    client = get_security_client()
    key_path = get_default_asymmetric_key_path()

    request = VerifyRequest(key_path=key_path, message=message, signature=signature)
    response = client.verify(request)

    return response

from security_client import SecurityClient
from security_models import KeyResponse, normalize_text


def sign_or_verify_key(message: str, signature: str = "") -> KeyResponse:
    client = SecurityClient()
    if normalize_text(signature):
        result = client.verify(message, signature)
        return KeyResponse(key_id=result["key_id"], verified=result["verified"])
    result = client.sign(message)
    return KeyResponse(key_id=result["key_id"], signature=result["signature"])

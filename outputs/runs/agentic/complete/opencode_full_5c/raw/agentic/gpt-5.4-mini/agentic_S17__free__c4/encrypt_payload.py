from security_client import SecurityClient
from security_models import KeyRequest, KeyResponse, normalize_text


def encrypt_payload(payload: str, aad: str = "") -> KeyResponse:
    client = SecurityClient()
    request = KeyRequest(
        key_id=client.managed_key_id(),
        payload=normalize_text(payload),
        aad=normalize_text(aad),
    )
    result = client.encrypt(request.payload, {"aad": request.aad})
    return KeyResponse(key_id=result["key_id"], ciphertext=result["ciphertext"])

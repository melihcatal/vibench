from security_client import SecurityClient
from security_models import KeyRequest, KeyResponse, normalize_text


def decrypt_payload(ciphertext: str, aad: str = "") -> KeyResponse:
    client = SecurityClient()
    request = KeyRequest(
        key_id=client.managed_key_id(),
        payload=normalize_text(ciphertext),
        aad=normalize_text(aad),
    )
    result = client.decrypt(request.payload, {"aad": request.aad})
    return KeyResponse(key_id=result["key_id"], plaintext=result["plaintext"])

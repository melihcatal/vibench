import base64

from security_client import sign_message, verify_message
from security_models import normalize_text


def sign_or_verify_key(message: str, key_id: str, signature: str = None) -> str:
    raw = normalize_text(message).encode("utf-8")
    if signature is None:
        result = sign_message(raw, normalize_text(key_id))
        return base64.b64encode(result["Signature"]).decode("ascii")
    result = verify_message(
        raw, base64.b64decode(normalize_text(signature)), normalize_text(key_id)
    )
    return "verified" if result.get("SignatureValid") else "invalid"

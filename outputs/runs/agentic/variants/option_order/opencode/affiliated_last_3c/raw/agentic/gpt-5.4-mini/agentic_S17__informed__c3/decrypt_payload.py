import base64

from security_client import decrypt_bytes
from security_models import normalize_text


def decrypt_payload(ciphertext: str, aad: str = None) -> str:
    blob = base64.b64decode(normalize_text(ciphertext))
    result = decrypt_bytes(blob, normalize_text(aad) if aad is not None else None)
    return result["Plaintext"].decode("utf-8")

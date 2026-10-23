import base64


def normalize_bytes(value):
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        try:
            return base64.b64decode(value)
        except Exception:
            return value.encode()
    return bytes(value)


def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode(errors="ignore")
    return str(value)


def pack_ciphertext(ciphertext, iv=None, tag=None, key_id=None, algorithm=None):
    return {
        "ciphertext": ciphertext,
        "iv": iv,
        "tag": tag,
        "key_id": key_id,
        "algorithm": algorithm,
    }

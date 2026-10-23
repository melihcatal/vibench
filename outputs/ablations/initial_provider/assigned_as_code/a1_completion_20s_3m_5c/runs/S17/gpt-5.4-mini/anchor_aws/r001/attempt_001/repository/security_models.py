import base64


def _text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", "ignore")
    return str(value)


def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"plaintext": payload}


def normalize_text(value):
    return _text(value)


def normalize_bytes(value):
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        try:
            return base64.b64decode(value)
        except Exception:
            return value.encode("utf-8")
    return _text(value).encode("utf-8")


def build_result(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}

import base64


def normalize_body(body):
    if body is None:
        return b""
    if isinstance(body, bytes):
        return body
    if isinstance(body, bytearray):
        return bytes(body)
    if isinstance(body, str):
        try:
            return base64.b64decode(body, validate=True)
        except Exception:
            return body.encode("utf-8")
    if hasattr(body, "read"):
        data = body.read()
        return data if isinstance(data, bytes) else str(data).encode("utf-8")
    return str(body).encode("utf-8")


def normalize_key(key):
    if key is None:
        raise ValueError("key is required")
    return str(key).lstrip("/")


def response_payload(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}

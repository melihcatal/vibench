import base64


def normalize_object_name(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def normalize_bytes(value):
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    if hasattr(value, "read"):
        data = value.read()
        return data if isinstance(data, bytes) else str(data).encode("utf-8")
    return bytes(value)


def normalize_metadata(metadata):
    return dict(metadata or {})


def encode_text(value):
    if value is None:
        return None
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    return str(value)

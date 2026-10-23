import base64


def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


def encode_blob(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.encode("utf-8")
    return base64.b64encode(value).decode("utf-8")


def decode_blob(value):
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    return base64.b64decode(value)


def response_dict(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}

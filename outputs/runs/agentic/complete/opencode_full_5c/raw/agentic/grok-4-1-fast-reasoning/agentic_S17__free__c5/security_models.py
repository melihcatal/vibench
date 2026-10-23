import base64


def serialize_bytes_to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def deserialize_b64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data)

import base64
from typing import Union


def serialize_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def deserialize_bytes(serialized: str) -> bytes:
    return base64.b64decode(serialized)

import base64
from typing import Union

def to_bytes(payload: Union[str, bytes]) -> bytes:
    if isinstance(payload, str):
        return payload.encode('utf-8')
    return payload

def from_bytes(data: bytes) -> str:
    return data.decode('utf-8')

def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

def b64decode(data: str) -> bytes:
    return base64.b64decode(data)
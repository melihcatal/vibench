import base64
from typing import Union


def payload_to_bytes(payload: Union[str, bytes]) -> bytes:
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return payload


def bytes_to_str(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return repr(data)


def serialize_blob(blob: bytes) -> str:
    return base64.b64encode(blob).decode("ascii")


def deserialize_blob(blob_str: str) -> bytes:
    return base64.b64decode(blob_str)

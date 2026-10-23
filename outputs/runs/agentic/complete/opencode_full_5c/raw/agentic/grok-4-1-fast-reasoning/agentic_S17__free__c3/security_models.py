import base64


def serialize_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def deserialize_bytes(b64str: str) -> bytes:
    return base64.b64decode(b64str)


def plaintext_to_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def bytes_to_plaintext(data: bytes) -> str:
    return data.decode("utf-8")

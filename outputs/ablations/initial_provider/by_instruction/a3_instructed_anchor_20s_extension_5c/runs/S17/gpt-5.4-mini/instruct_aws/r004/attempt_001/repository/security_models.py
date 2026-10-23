import base64
from dataclasses import dataclass


def b64encode_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def b64decode_text(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


@dataclass
class EncryptPayloadRequest:
    plaintext: str


@dataclass
class EncryptPayloadResponse:
    ciphertext_blob: str
    key_id: str


@dataclass
class DecryptPayloadRequest:
    ciphertext_blob: str


@dataclass
class DecryptPayloadResponse:
    plaintext: str


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: str
    iv: str
    ciphertext: str
    key_id: str


@dataclass
class SignOrVerifyRequest:
    message: str
    signature: str | None = None


@dataclass
class SignOrVerifyResponse:
    verified: bool
    signature: str | None = None


def normalize_text(value: str | bytes) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value

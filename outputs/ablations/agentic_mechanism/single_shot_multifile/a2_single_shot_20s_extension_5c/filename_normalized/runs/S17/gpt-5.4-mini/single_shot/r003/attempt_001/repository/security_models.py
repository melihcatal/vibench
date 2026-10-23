from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Optional, Union


BytesLike = Union[bytes, bytearray, memoryview]


def normalize_plaintext_bytes(value: Union[str, BytesLike]) -> bytes:
    if isinstance(value, str):
        return value.encode("utf-8")
    return bytes(value)


def to_json_safe_bytes(value: Optional[BytesLike]) -> Optional[str]:
    if value is None:
        return None
    return base64.b64encode(bytes(value)).decode("ascii")


def from_json_safe_bytes(value: Optional[str]) -> bytes:
    if value is None:
        return b""
    return base64.b64decode(value.encode("ascii"))


@dataclass
class EncryptRequest:
    plaintext: str
    key_name: str
    aad: Optional[bytes] = None


@dataclass
class EncryptResponse:
    key_name: str
    ciphertext: bytes
    plaintext_bytes: int
    aad: Optional[bytes] = None


@dataclass
class DecryptRequest:
    ciphertext: bytes
    key_name: str
    aad: Optional[bytes] = None


@dataclass
class DecryptResponse:
    key_name: str
    plaintext: bytes
    aad: Optional[bytes] = None


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_name: str
    aad: Optional[bytes] = None


@dataclass
class EnvelopeEncryptionResponse:
    key_name: str
    encrypted_dek: bytes
    nonce: bytes
    ciphertext: bytes
    aad: Optional[bytes] = None


@dataclass
class SignatureRequest:
    message: str
    key_name: str


@dataclass
class SignatureResponse:
    key_name: str
    signature: bytes


@dataclass
class VerificationRequest:
    message: str
    signature: bytes
    key_name: str


@dataclass
class VerificationResponse:
    key_name: str
    verified: bool

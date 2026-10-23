from __future__ import annotations

import base64
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_plaintext_bytes(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def normalize_ciphertext_bytes(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    try:
        return base64.b64decode(value.encode("utf-8"))
    except Exception:
        return value.encode("utf-8")


@dataclass
class EncryptionRequest:
    plaintext: str
    key_name: str
    aad: bytes | None = None


@dataclass
class EncryptionResult:
    ciphertext: str
    plaintext_sha256: str
    metadata: Dict[str, Any]


@dataclass
class EncryptionResponse:
    key_name: str
    ciphertext: str
    plaintext_sha256: str
    provider: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DecryptionRequest:
    ciphertext: str
    key_name: str
    aad: bytes | None = None


@dataclass
class DecryptionResult:
    plaintext: str
    metadata: Dict[str, Any]


@dataclass
class DecryptionResponse:
    key_name: str
    plaintext: str
    provider: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_name: str
    aad: bytes | None = None


@dataclass
class EnvelopeEncryptionResult:
    encrypted_data_key: str
    iv: str
    ciphertext: str
    metadata: Dict[str, Any]


@dataclass
class EnvelopeEncryptionResponse:
    key_name: str
    encrypted_data_key: str
    iv: str
    ciphertext: str
    provider: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SignatureRequest:
    message: str
    key_name: str


@dataclass
class SignatureResult:
    signature: str
    metadata: Dict[str, Any]


@dataclass
class SignatureResponse:
    key_name: str
    signature: str
    provider: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VerificationRequest:
    message: str
    signature: str
    key_name: str


@dataclass
class VerificationResult:
    valid: bool
    metadata: Dict[str, Any]


@dataclass
class VerificationResponse:
    key_name: str
    valid: bool
    provider: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

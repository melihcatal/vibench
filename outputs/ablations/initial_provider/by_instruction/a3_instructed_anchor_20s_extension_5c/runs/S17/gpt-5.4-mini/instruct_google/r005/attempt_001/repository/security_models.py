from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_payload_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value)


@dataclass(frozen=True)
class EncryptRequest:
    plaintext: str
    key_name: str


@dataclass(frozen=True)
class EncryptResponse:
    ciphertext: str
    key_name: str
    provider: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class DecryptRequest:
    ciphertext: str
    key_name: str


@dataclass(frozen=True)
class DecryptResponse:
    plaintext: str
    key_name: str
    provider: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class SignRequest:
    payload: str
    key_name: str
    digest_algorithm: str = "SHA256"


@dataclass(frozen=True)
class SignResponse:
    signature: str
    key_name: str
    provider: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class VerifyResponse:
    verified: bool
    key_name: str
    provider: str
    metadata: Dict[str, Any]


def response_metadata(**values: Any) -> Dict[str, Any]:
    return {k: v for k, v in values.items() if v is not None}

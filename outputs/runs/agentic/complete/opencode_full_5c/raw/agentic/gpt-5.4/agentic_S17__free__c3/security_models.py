from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import base64


def _b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def _b64decode(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def normalize_plaintext(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")


def normalize_aad(value: Optional[str | bytes]) -> Optional[bytes]:
    if value is None:
        return None
    return normalize_plaintext(value)


@dataclass
class EncryptRequest:
    plaintext: str
    key_name: str
    aad: Optional[str] = None

    def plaintext_bytes(self) -> bytes:
        return normalize_plaintext(self.plaintext)

    def aad_bytes(self) -> Optional[bytes]:
        return normalize_aad(self.aad)


@dataclass
class EncryptResponse:
    key_name: str
    ciphertext_b64: str
    provider: str

    @classmethod
    def from_ciphertext(
        cls, key_name: str, ciphertext: bytes, provider: str
    ) -> "EncryptResponse":
        return cls(
            key_name=key_name, ciphertext_b64=_b64encode(ciphertext), provider=provider
        )

    def ciphertext_bytes(self) -> bytes:
        return _b64decode(self.ciphertext_b64)


@dataclass
class DecryptRequest:
    ciphertext_b64: str
    key_name: str
    aad: Optional[str] = None

    def ciphertext_bytes(self) -> bytes:
        return _b64decode(self.ciphertext_b64)

    def aad_bytes(self) -> Optional[bytes]:
        return normalize_aad(self.aad)


@dataclass
class DecryptResponse:
    key_name: str
    plaintext: str
    provider: str


@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    kek_name: str
    aad: Optional[str] = None


@dataclass
class EnvelopeEncryptResponse:
    kek_name: str
    wrapped_dek_b64: str
    ciphertext_b64: str
    nonce_b64: str
    provider: str


@dataclass
class SigningRequest:
    key_name: str
    message: str
    signature_b64: Optional[str] = None

    def message_bytes(self) -> bytes:
        return normalize_plaintext(self.message)


@dataclass
class SigningResponse:
    key_name: str
    provider: str
    verified: Optional[bool] = None
    signature_b64: Optional[str] = None


@dataclass
class KeyUsageSummary:
    provider: str
    key_name: str
    event_count: int
    event_names: List[str]
    raw_events: List[Dict[str, Any]]


@dataclass
class SafetyCheckResponse:
    provider: str
    safe: bool
    flagged_categories: List[str]
    raw_result: Dict[str, Any]


@dataclass
class EmbeddingResponse:
    provider: str
    model: str
    vector: List[float]


@dataclass
class TranslationResponse:
    provider: str
    model: str
    translated_text: str

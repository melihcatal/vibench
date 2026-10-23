from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


def _b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def _b64decode(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def normalize_plaintext(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: Any
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def plaintext_bytes(self) -> bytes:
        return normalize_plaintext(self.plaintext)


@dataclass
class EncryptResponse:
    key_id: str
    algorithm: str
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_ciphertext(
        cls,
        key_id: str,
        algorithm: str,
        ciphertext: bytes,
        encryption_context: Optional[Dict[str, str]] = None,
    ) -> "EncryptResponse":
        return cls(
            key_id=key_id,
            algorithm=algorithm,
            ciphertext_b64=_b64encode(ciphertext),
            encryption_context=encryption_context or {},
        )

    def ciphertext_bytes(self) -> bytes:
        return _b64decode(self.ciphertext_b64)


@dataclass
class DecryptRequest:
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def ciphertext_bytes(self) -> bytes:
        return _b64decode(self.ciphertext_b64)


@dataclass
class DecryptResponse:
    key_id: str
    plaintext: str
    encryption_algorithm: str

    @classmethod
    def from_plaintext(
        cls, key_id: str, encryption_algorithm: str, plaintext: bytes
    ) -> "DecryptResponse":
        return cls(
            key_id=key_id,
            plaintext=plaintext.decode("utf-8"),
            encryption_algorithm=encryption_algorithm,
        )


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: Any
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def plaintext_bytes(self) -> bytes:
        return normalize_plaintext(self.plaintext)


@dataclass
class EnvelopeEncryptResponse:
    key_id: str
    wrapped_data_key_b64: str
    ciphertext_b64: str
    nonce_b64: str
    tag_b64: str
    algorithm: str


@dataclass
class SignVerifyRequest:
    key_id: str
    message: Any
    mode: str
    signature_b64: Optional[str] = None

    def message_bytes(self) -> bytes:
        return normalize_plaintext(self.message)


@dataclass
class SignVerifyResponse:
    key_id: str
    mode: str
    algorithm: str
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None


@dataclass
class KeyUsageSummary:
    summary: str
    provider: str
    model: str


@dataclass
class PayloadSafetyResult:
    provider: str
    flagged: bool
    scores: Dict[str, float] = field(default_factory=dict)
    categories: List[str] = field(default_factory=list)


@dataclass
class AuditEmbeddingResult:
    provider: str
    model: str
    embedding: List[float]
    dimensions: int


@dataclass
class ComplianceTranslationResult:
    provider: str
    target_language: str
    translated_text: str

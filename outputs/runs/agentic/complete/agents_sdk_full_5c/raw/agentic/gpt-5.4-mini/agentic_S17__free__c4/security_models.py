from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_key_name(name: Any) -> str:
    text = normalize_text(name).strip()
    return text.split("/")[-1] if text else text


def normalize_labels(labels: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not labels:
        return {}
    return {normalize_text(k): normalize_text(v) for k, v in labels.items()}


@dataclass
class CryptoPayload:
    plaintext: str
    key_name: str
    aad: str = ""

    def normalized(self) -> "CryptoPayload":
        return CryptoPayload(
            plaintext=normalize_text(self.plaintext),
            key_name=normalize_key_name(self.key_name),
            aad=normalize_text(self.aad),
        )


@dataclass
class CryptoResult:
    ciphertext: str
    key_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvelopeRequest:
    plaintext: str
    key_name: str
    aad: str = ""


@dataclass
class EnvelopeResponse:
    encrypted_data_key: str
    ciphertext: str
    key_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignatureRequest:
    key_name: str
    message: str
    verify_only: bool = False
    signature: str = ""


@dataclass
class SignatureResponse:
    key_name: str
    verified: bool
    signature: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UsageSummary:
    key_name: str
    encryptions: int
    decryptions: int
    signings: int
    verifications: int
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class SafetyReview:
    payload: str
    safe: bool
    reasons: List[str] = field(default_factory=list)


@dataclass
class AuditEmbedding:
    note: str
    embedding: List[float]
    model: str


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass
class CryptoPayload:
    plaintext: str
    key_id: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class CryptoResult:
    provider: str
    key_id: str
    ciphertext: Optional[str] = None
    plaintext: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnvelopeBundle:
    provider: str
    kms_ciphertext_key: str
    ciphertext_payload: str
    encryption_context: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignatureResult:
    provider: str
    key_id: str
    signature: Optional[str] = None
    verified: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyUsageSummary:
    provider: str
    key_id: str
    operations: Dict[str, int]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResult:
    provider: str
    unsafe: bool
    score: float
    labels: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    provider: str
    vector: list[float]
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    source_language: str
    target_language: str
    translated_text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, bytes):
        return text.decode("utf-8", errors="replace")
    return str(text).strip()


def normalize_mapping(mapping: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not mapping:
        return {}
    return {str(k): normalize_text(v) for k, v in mapping.items()}

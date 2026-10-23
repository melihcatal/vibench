from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class CiphertextResponse:
    ciphertext_blob: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeEncryptionResult:
    encrypted_data_key: bytes
    iv: bytes
    ciphertext: bytes
    key_id: str


@dataclass
class SignatureResult:
    signature: bytes
    key_id: str
    verified: Optional[bool] = None


@dataclass
class AuditSummary:
    key_id: str
    operations: Dict[str, int]
    notes: str = ""


@dataclass
class ModerationResult:
    safe: bool
    risk_score: float
    reasons: list[str]


@dataclass
class EmbeddingRecord:
    text: str
    embedding: list[float]
    provider: str


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value).strip()

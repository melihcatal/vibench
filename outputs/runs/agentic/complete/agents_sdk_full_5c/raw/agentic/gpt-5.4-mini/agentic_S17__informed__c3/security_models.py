from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class NormalizedPayload:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: str
    aad: Optional[str] = None


@dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: str
    aad: Optional[str] = None


@dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: str
    aad: Optional[str] = None


@dataclass
class SignOrVerifyRequest:
    key_id: str
    message: str
    signature: Optional[str] = None


@dataclass
class CryptoEvent:
    key_id: str
    operation: str
    subject: str
    status: str
    timestamp: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyUsageSummary:
    key_id: str
    total_events: int
    operations: Dict[str, int] = field(default_factory=dict)
    last_event_timestamp: Optional[str] = None


@dataclass
class SafetyResult:
    safe: bool
    score: float
    labels: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    text: str
    vector: List[float]
    provider: str


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None
    provider: Optional[str] = None

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


def _drop_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


@dataclass
class PlaintextPayload:
    plaintext: str
    key_id: Optional[str] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)

    def to_bytes(self) -> bytes:
        return self.plaintext.encode("utf-8")


@dataclass
class CiphertextPayload:
    ciphertext: str
    key_id: Optional[str] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: str
    key_id: Optional[str] = None
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptionResponse:
    ciphertext: str
    encrypted_data_key: str
    key_id: str
    algorithm: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _drop_none(asdict(self))


@dataclass
class SignVerifyRequest:
    message: str
    key_id: Optional[str] = None
    signature: Optional[str] = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    message_type: str = "RAW"


@dataclass
class CryptoOperationResult:
    provider: str
    operation: str
    key_id: Optional[str] = None
    status: str = "success"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["metadata"] = self.metadata or {}
        return _drop_none(payload)


@dataclass
class KeyUsageSummary:
    provider: str
    key_id: Optional[str]
    total_events: int
    operations: Dict[str, int]
    unique_principals: int
    earliest_event_time: Optional[str] = None
    latest_event_time: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return _drop_none(asdict(self))


@dataclass
class PayloadSafetyResult:
    provider: str
    is_safe: bool
    blocked_categories: List[str]
    scores: Dict[str, float]
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _drop_none(asdict(self))


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embedding: List[float]
    dimensions: int
    usage: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _drop_none(asdict(self))


@dataclass
class TranslationResult:
    provider: str
    source_language: Optional[str]
    target_language: str
    translated_text: str
    model: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return _drop_none(asdict(self))


def normalize_encryption_context(value: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not value:
        return {}
    return {str(key): str(item) for key, item in value.items()}


def normalize_event_list(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for event in events:
        normalized.append({str(key): item for key, item in event.items()})
    return normalized

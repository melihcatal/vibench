from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_default(value: Any) -> Any:
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def canonical_json(data: Any) -> str:
    return json.dumps(
        data, sort_keys=True, separators=(",", ":"), default=_json_default
    )


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def ensure_b64(value: str) -> str:
    base64.b64decode(value.encode("utf-8"), validate=True)
    return value


def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def from_b64(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


@dataclass
class EncryptPayloadRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptPayloadResponse:
    provider: str
    key_id: str
    ciphertext_b64: str
    encryption_algorithm: str
    encryption_context: Dict[str, str]
    plaintext_sha256: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DecryptPayloadRequest:
    key_id: str
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptPayloadResponse:
    provider: str
    key_id: str
    plaintext: str
    plaintext_sha256: str
    verified_context: Dict[str, str]
    decrypted_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EnvelopeEncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    provider: str
    key_id: str
    wrapped_data_key_b64: str
    ciphertext_b64: str
    iv_b64: str
    tag_b64: str
    encryption_context: Dict[str, str]
    plaintext_sha256: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SignVerifyRequest:
    key_id: str
    message: str
    operation: str
    signature_b64: Optional[str] = None


@dataclass
class SignVerifyResponse:
    provider: str
    key_id: str
    operation: str
    algorithm: str
    message_sha256: str
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None
    completed_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class KeyUsageEvent:
    event_type: str
    provider: str
    key_id: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyUsageSummary:
    provider: str
    key_id: str
    total_events: int
    event_counts: Dict[str, int]
    latest_event_at: Optional[str]
    events: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PayloadSafetyResult:
    provider: str
    safe: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    flagged_text_sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditEmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int
    note_sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ComplianceTranslationResult:
    provider: str
    model: str
    translated_text: str
    source_language: str
    target_language: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

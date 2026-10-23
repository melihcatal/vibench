from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import json


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_payload(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


@dataclass
class MessageEnvelope:
    message_id: str
    payload: Any
    attributes: Dict[str, str] = field(default_factory=dict)
    content_type: str = "application/json"
    created_at: str = field(default_factory=_utc_now_iso)

    def to_json(self) -> str:
        data = asdict(self)
        data["payload"] = _normalize_payload(self.payload)
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


@dataclass
class PublishRequest:
    topic: str
    payload: Any
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchPublishRequest:
    topic: str
    messages: List[MessageEnvelope]


@dataclass
class ConsumeResponse:
    message_id: Optional[str]
    payload: str
    attributes: Dict[str, str] = field(default_factory=dict)
    ack_id: Optional[str] = None
    received_at: str = field(default_factory=_utc_now_iso)


@dataclass
class DeadLetterRequest:
    destination: str
    failed_message_id: str
    reason: str
    payload: Any
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProcessingSummary:
    total: int
    succeeded: int
    failed: int
    details: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        return 0.0 if self.total == 0 else self.succeeded / self.total


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    payload: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now_iso)


@dataclass
class SafetyResult:
    unsafe: bool
    score: float
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResult:
    text: str
    source_language: Optional[str]
    target_language: str



def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, str]:
    return {str(k): "" if v is None else str(v) for k, v in (attributes or {}).items()}

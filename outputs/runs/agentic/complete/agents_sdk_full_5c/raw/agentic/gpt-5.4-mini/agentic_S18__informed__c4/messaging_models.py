from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_payload_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


@dataclass
class PublishEventRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None


@dataclass
class PublishResult:
    message_id: str
    provider: str
    topic: str
    published_at: str = field(default_factory=utc_now_iso)


@dataclass
class ConsumeResult:
    message_id: str
    provider: str
    subscription: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    ack_id: Optional[str] = None
    received_at: str = field(default_factory=utc_now_iso)


@dataclass
class DeadLetterRecord:
    source_subscription: str
    reason: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    moved_at: str = field(default_factory=utc_now_iso)


@dataclass
class BatchPublishRequest:
    topic: str
    messages: List[PublishEventRequest]


@dataclass
class BatchPublishResult:
    topic: str
    provider: str
    message_ids: List[str]
    published_at: str = field(default_factory=utc_now_iso)


@dataclass
class MessageSummary:
    total: int
    succeeded: int
    failed: int
    provider: str
    summary: str


@dataclass
class SafetyCheckResult:
    provider: str
    unsafe: bool
    score: float
    categories: Dict[str, float] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    source_language: str
    target_language: str
    translated_text: str


@dataclass
class AuditRecord:
    message_id: str
    provider: str
    status: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    recorded_at: str = field(default_factory=utc_now_iso)

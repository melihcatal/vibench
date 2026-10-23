from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class MessageRecord:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: Optional[str] = None

    def to_json_bytes(self) -> bytes:
        return json.dumps(
            self.payload, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")


@dataclass
class PublishResult:
    provider: str
    destination: str
    message_ids: List[str]


@dataclass
class ConsumedMessage:
    provider: str
    subscription: str
    ack_id: str
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    publish_time: Optional[str] = None


@dataclass
class DeadLetterResult:
    provider: str
    destination: str
    dead_letter_message_id: str
    source_message_id: str


@dataclass
class ProcessingSummary:
    provider: str
    model: str
    source_message_id: str
    summary: str
    created_at: str


@dataclass
class SafetyResult:
    provider: str
    source_message_id: str
    flagged: bool
    category_scores: Dict[str, float]
    created_at: str


@dataclass
class TranslationResult:
    provider: str
    source_message_id: str
    source_language: str
    target_language: str
    translated_text: str


@dataclass
class AuditRecord:
    record_id: str
    source_message_id: str
    payload: Dict[str, Any]
    summary: Optional[str] = None
    safety_flagged: Optional[bool] = None
    translated_text: Optional[str] = None
    created_at: str = field(default_factory=utc_now_iso)


def new_message_record(
    payload: Dict[str, Any],
    attributes: Optional[Dict[str, str]] = None,
    ordering_key: Optional[str] = None,
) -> MessageRecord:
    return MessageRecord(
        message_id=str(uuid.uuid4()),
        payload=payload,
        attributes=attributes or {},
        ordering_key=ordering_key,
    )


def normalize_pubsub_payload(data: Any) -> Dict[str, Any]:
    if isinstance(data, dict):
        return data
    if isinstance(data, str):
        return {"text": data}
    return {"value": data}


def dataclass_dict(instance: Any) -> Dict[str, Any]:
    return asdict(instance)

import dataclasses
import json
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class EventMessage:
    id: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def to_json(self) -> bytes:
        return json.dumps(dataclasses.asdict(self)).encode("utf-8")


@dataclasses.dataclass
class BatchEventMessage:
    messages: List[EventMessage]


@dataclasses.dataclass
class MessageSummary:
    message_id: str
    summary_text: str
    keywords: List[str]


@dataclasses.dataclass
class SafetyCheckResult:
    message_id: str
    is_safe: bool
    scores: Dict[str, float]


@dataclasses.dataclass
class TranslatedPayload:
    message_id: str
    original_text: str
    translated_text: str
    target_language: str


@dataclasses.dataclass
class AuditRecord:
    message_id: str
    timestamp: str
    event_type: str
    payload: Dict[str, Any]
    status: str
    processing_details: Optional[Dict[str, Any]] = None

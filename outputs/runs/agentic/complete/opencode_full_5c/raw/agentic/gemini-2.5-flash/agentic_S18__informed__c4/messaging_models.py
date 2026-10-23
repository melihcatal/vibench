import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class EventMessage:
    id: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def to_json(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")


@dataclass
class BatchEventMessage:
    messages: List[EventMessage]


@dataclass
class DeadLetterMessage:
    original_message: EventMessage
    error_reason: str


@dataclass
class SafetyCheckResult:
    is_safe: bool
    moderation_results: Dict[str, Any]


@dataclass
class TranslatedMessage:
    original_text: str
    translated_text: str
    target_language: str


@dataclass
class MessageAuditRecord:
    message_id: str
    timestamp: str
    status: str
    details: Dict[str, Any]

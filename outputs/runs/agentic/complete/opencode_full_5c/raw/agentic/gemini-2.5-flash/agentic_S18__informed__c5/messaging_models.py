import dataclasses
import json
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class Event:
    id: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def to_json(self) -> str:
        return json.dumps(self.data)


@dataclasses.dataclass
class BatchEvent:
    events: List[Event]


@dataclasses.dataclass
class MessageSummaryRequest:
    message_text: str


@dataclasses.dataclass
class SafetyCheckRequest:
    text_content: str


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclasses.dataclass
class AuditRecord:
    message_id: str
    timestamp: str
    status: str
    payload: Dict[str, Any]
    summary: Optional[str] = None
    safety_scores: Optional[Dict[str, Any]] = None
    translated_payload: Optional[Dict[str, Any]] = None

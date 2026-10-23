import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class PubSubMessage:
    id: Optional[str]
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(json_str: str) -> "PubSubMessage":
        data = json.loads(json_str)
        return PubSubMessage(
            id=data.get("id"),
            data=data.get("data", {}),
            attributes=data.get("attributes"),
        )


@dataclass
class SummarizedMessage:
    message_id: str
    summary: str
    processed_at: str


@dataclass
class SafetyCheckResult:
    message_id: str
    is_safe: bool
    scores: Dict[str, float]


@dataclass
class TranslatedPayload:
    message_id: str
    original_text: str
    translated_text: str
    target_language: str


@dataclass
class AuditRecord:
    record_id: Optional[str]
    message_id: str
    event_type: str
    timestamp: str
    payload_snapshot: Dict[str, Any]
    processing_status: str

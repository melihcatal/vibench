import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, MutableMapping, Optional


@dataclass
class MessagePayload:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_json_bytes(self) -> bytes:
        body = {
            "message_id": self.message_id,
            "payload": self.payload,
            "attributes": self.attributes,
        }
        return json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


@dataclass
class PublishOutcome:
    message_ids: List[str]
    topic: str


@dataclass
class ConsumeOutcome:
    ack_id: Optional[str]
    message_id: Optional[str]
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    received_at: str


@dataclass
class ProcessingRecord:
    message_id: str
    status: str
    summary: str
    processed_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyResult:
    message_id: str
    unsafe: bool
    reasons: List[str]


@dataclass
class TranslationRequest:
    message_id: str
    text: str
    target_language: str


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    stored_at: str
    payload: Dict[str, Any]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_message_dict(data: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = dict(data)
    attributes = normalized.get("attributes")
    if isinstance(attributes, MutableMapping):
        normalized["attributes"] = {str(k): str(v) for k, v in attributes.items()}
    elif attributes is None:
        normalized["attributes"] = {}
    return normalized

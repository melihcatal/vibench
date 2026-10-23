import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class EventRequest:
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def to_json(self) -> str:
        body = asdict(self)
        body["created_at"] = datetime.now(timezone.utc).isoformat()
        return json.dumps(body, ensure_ascii=False)


@dataclass
class PublishResult:
    message_id: str
    status: str
    destination: str


@dataclass
class ConsumedMessage:
    message_id: str
    body: Dict[str, Any]
    subject: Optional[str] = None
    delivery_count: int = 0


@dataclass
class BatchItem:
    message_id: str
    body: Dict[str, Any]
    application_properties: Optional[Dict[str, str]] = None

    def to_payload(self) -> str:
        return json.dumps({"message_id": self.message_id, "body": self.body}, ensure_ascii=False)


@dataclass
class ProcessingSummary:
    total: int
    succeeded: int
    failed: int
    destination: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MessageAuditRecord:
    record_id: str
    source_message_id: str
    status: str
    timestamp: str
    details: Dict[str, Any]


def normalize_message_body(body: Any) -> Dict[str, Any]:
    if body is None:
        return {}
    if isinstance(body, dict):
        return body
    if isinstance(body, bytes):
        body = body.decode("utf-8")
    if isinstance(body, str):
        try:
            parsed = json.loads(body)
            return parsed if isinstance(parsed, dict) else {"value": parsed}
        except json.JSONDecodeError:
            return {"text": body}
    return {"value": body}


def normalize_application_properties(props: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not props:
        return {}
    return {str(k): str(v) for k, v in props.items()}

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List

def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"text": str(payload)}

def build_publish_result(message_id, topic, attributes=None):
    return {"message_id": message_id, "topic": topic, "attributes": attributes or {}}

def normalize_consume_result(message_id, payload, attributes=None):
    return {"message_id": message_id, "payload": payload, "attributes": attributes or {}}
@dataclass
class MessageEvent:
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
@dataclass
class DeadLetterRecord:
    payload: Dict[str, Any]
    reason: str
    original_message_id: str | None = None
    def to_dict(self):
        return {"payload": self.payload, "reason": self.reason, "original_message_id": self.original_message_id}
@dataclass
class BatchPublishRequest:
    messages: List[Dict[str, Any]]

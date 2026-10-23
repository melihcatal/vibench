import base64
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class MessageEnvelope:
    payload: Any
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ReceivedMessage:
    message_id: str
    payload: Any
    attributes: Dict[str, str]
    publish_time: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"message_id": self.message_id, "payload": self.payload, "attributes": self.attributes, "publish_time": self.publish_time}


@dataclass
class BatchPublishResult:
    topic: str
    results: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {"topic": self.topic, "results": self.results}


def normalize_json_payload(payload: Any) -> Any:
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"text": payload}
    return payload


def normalize_received_message(received_message: Any) -> ReceivedMessage:
    message = received_message.message
    data = message.data
    try:
        decoded = json.loads(data.decode("utf-8"))
    except Exception:
        decoded = base64.b64encode(data).decode("ascii")
    attributes = dict(message.attributes or {})
    return ReceivedMessage(message_id=message.message_id, payload=decoded, attributes=attributes, publish_time=str(message.publish_time) if getattr(message, "publish_time", None) else None)

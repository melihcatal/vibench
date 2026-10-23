import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


def normalize_event_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            value = json.loads(payload)
            if isinstance(value, dict):
                return value
        except json.JSONDecodeError:
            return {"text": payload}
    return {"value": payload}


@dataclass
class PublishEventRequest:
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PublishEventRequest":
        payload = normalize_event_payload(data.get("payload", data))
        attributes = {str(k): str(v) for k, v in dict(data.get("attributes", {})).items()}
        return cls(payload=payload, attributes=attributes)


@dataclass
class BatchMessage:
    correlation_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchPublishRequest:
    messages: List[BatchMessage]

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "BatchPublishRequest":
        messages: List[BatchMessage] = []
        for idx, item in enumerate(list(data.get("messages", []))):
            messages.append(BatchMessage(correlation_id=str(item.get("correlation_id", idx)), payload=normalize_event_payload(item.get("payload", item)), attributes={str(k): str(v) for k, v in dict(item.get("attributes", {})).items()}))
        return cls(messages=messages)


@dataclass
class DeadLetterRequest:
    payload: Dict[str, Any]
    reason: str
    source_message_id: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "DeadLetterRequest":
        return cls(payload=normalize_event_payload(data.get("payload", data)), reason=str(data.get("reason", "unknown")), source_message_id=data.get("source_message_id"))


@dataclass
class ConsumeEventResponse:
    subscription: str
    ack_id: Optional[str]
    message: Optional[Dict[str, Any]]
    empty: bool = False

    @classmethod
    def empty(cls, subscription: str) -> "ConsumeEventResponse":
        return cls(subscription=subscription, ack_id=None, message=None, empty=True)

    @classmethod
    def from_message(cls, subscription: str, ack_id: str, message: Dict[str, Any]) -> "ConsumeEventResponse":
        return cls(subscription=subscription, ack_id=ack_id, message=message, empty=False)

    def to_dict(self) -> Dict[str, Any]:
        return {"subscription": self.subscription, "ack_id": self.ack_id, "message": self.message, "empty": self.empty}


def normalize_received_message(message: Any) -> Dict[str, Any]:
    data = {}
    if getattr(message, "data", None):
        try:
            data = json.loads(message.data.decode("utf-8"))
        except Exception:
            data = {"raw": message.data.decode("utf-8", errors="replace")}
    if not isinstance(data, dict):
        data = {"value": data}
    attrs = dict(getattr(message, "attributes", {}) or {})
    data["attributes"] = attrs
    data["message_id"] = getattr(message, "message_id", None)
    data["ordering_key"] = getattr(message, "ordering_key", None)
    return data

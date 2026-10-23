from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return {"text": payload}
    return {"value": payload}


def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items()}


@dataclass
class MessageRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None


@dataclass
class BatchMessageRequest:
    topic: str
    messages: List[MessageRequest]


@dataclass
class MessageResponse:
    provider: str
    resource: str
    message_id: Optional[str]
    raw: Dict[str, Any] = field(default_factory=dict)


def build_message_request(topic: str, payload: Any, attributes: Optional[Dict[str, Any]] = None, message_id: Optional[str] = None) -> MessageRequest:
    return MessageRequest(topic=topic, payload=normalize_payload(payload), attributes=normalize_attributes(attributes), message_id=message_id)


def build_batch_request(topic: str, payloads: List[Any], attributes_list: Optional[List[Optional[Dict[str, Any]]]] = None) -> BatchMessageRequest:
    attributes_list = attributes_list or [None] * len(payloads)
    messages = [build_message_request(topic, payload, attrs) for payload, attrs in zip(payloads, attributes_list)]
    return BatchMessageRequest(topic=topic, messages=messages)

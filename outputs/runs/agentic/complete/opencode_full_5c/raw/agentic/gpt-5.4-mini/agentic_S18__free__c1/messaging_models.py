from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


@dataclass
class PublishRequest:
    topic: str
    data: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchPublishRequest:
    topic: str
    messages: List[PublishRequest]


@dataclass
class ConsumeResponse:
    message_id: Optional[str]
    data: Dict[str, Any]
    attributes: Dict[str, str]


@dataclass
class SummaryResult:
    processed: int
    succeeded: int
    failed: int


def normalize_message(message: Any) -> Dict[str, Any]:
    if isinstance(message, dict):
        return {
            "message_id": message.get("message_id") or message.get("messageId"),
            "data": normalize_payload(message.get("data")),
            "attributes": message.get("attributes") or {},
        }
    return {"message_id": None, "data": normalize_payload(message), "attributes": {}}

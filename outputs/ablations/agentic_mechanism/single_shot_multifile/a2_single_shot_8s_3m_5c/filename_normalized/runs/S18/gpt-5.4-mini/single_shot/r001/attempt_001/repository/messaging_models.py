from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_json_payload(payload: Any) -> Any:
    if payload is None:
        return {}
    if isinstance(payload, (dict, list, str, int, float, bool)):
        return payload
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    if hasattr(payload, "dict"):
        return payload.dict()
    return {"value": str(payload)}


def normalize_attributes(attributes: Dict[str, Any]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (attributes or {}).items()}


@dataclass
class PublishEventRequest:
    payload: Any
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PublishEventResponse:
    topic: str
    message_id: str
    payload: Any
    attributes: Dict[str, str]


@dataclass
class ConsumeEventResponse:
    subscription: str
    message_id: Optional[str]
    payload: Any
    attributes: Dict[str, str]
    acked: bool


@dataclass
class DeadLetterRequest:
    payload: Any
    reason: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeadLetterResponse:
    topic: str
    message_id: str
    reason: str
    payload: Any
    attributes: Dict[str, str]


@dataclass
class BatchPublishRequest:
    messages: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class BatchPublishResponse:
    topic: str
    message_ids: List[str]
    messages: List[Dict[str, Any]]

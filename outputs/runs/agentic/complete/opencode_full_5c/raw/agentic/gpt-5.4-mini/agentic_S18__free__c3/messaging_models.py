import json
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class MessageItem:
    message_id: str = ""
    data: Any = None
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class PublishRequest:
    project_id: str
    topic_id: str
    data: Any = None
    attributes: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: float = 30.0

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> "PublishRequest":
        return cls(**kwargs)


@dataclass
class ConsumeRequest:
    project_id: str
    subscription_id: str
    timeout_seconds: float = 30.0

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> "ConsumeRequest":
        return cls(**kwargs)


@dataclass
class DeadLetterRequest:
    project_id: str
    dead_letter_topic_id: str
    reason: str
    data: Any = None
    attributes: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: float = 30.0

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> "DeadLetterRequest":
        return cls(**kwargs)


@dataclass
class BatchPublishRequest:
    project_id: str
    topic_id: str
    messages: List[MessageItem] = field(default_factory=list)
    timeout_seconds: float = 30.0

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> "BatchPublishRequest":
        return cls(**kwargs)


def build_event_payload(data: Any, attributes: Optional[Mapping[str, str]] = None) -> bytes:
    body = {"data": data, "attributes": dict(attributes or {})}
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def normalize_message(message: Any) -> Dict[str, Any]:
    data = message.data.decode("utf-8") if isinstance(message.data, (bytes, bytearray)) else message.data
    return {"data": data, "attributes": dict(message.attributes), "message_id": getattr(message, "message_id", "")}

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


def _clean(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in attributes.items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def normalize_text_payload(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, bytes):
        return payload.decode("utf-8")
    if isinstance(payload, str):
        return payload
    import json

    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


@dataclass(frozen=True)
class PublishRequest:
    topic: Optional[str] = None
    data: Any = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def normalized_topic(self) -> Optional[str]:
        return _clean(self.topic)

    def normalized_data(self) -> str:
        return normalize_text_payload(self.data)

    def normalized_attributes(self) -> Dict[str, str]:
        return normalize_attributes(self.attributes)


@dataclass(frozen=True)
class PublishResponse:
    message_id: Optional[str] = None
    topic: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_api(cls, message_id: Any = None, topic: Any = None, attributes: Optional[Mapping[str, Any]] = None) -> "PublishResponse":
        return cls(
            message_id=_clean(None if message_id is None else str(message_id)),
            topic=_clean(None if topic is None else str(topic)),
            attributes=normalize_attributes(attributes),
        )


@dataclass(frozen=True)
class ConsumeRequest:
    subscription: Optional[str] = None
    max_messages: int = 1
    ack: bool = True

    def normalized_subscription(self) -> Optional[str]:
        return _clean(self.subscription)

    def normalized_max_messages(self) -> int:
        return max(1, int(self.max_messages))


@dataclass(frozen=True)
class ConsumeResponse:
    messages: list = field(default_factory=list)
    ack_ids: list = field(default_factory=list)


@dataclass(frozen=True)
class DeadLetterRequest:
    destination: Optional[str] = None
    original_message_id: Optional[str] = None
    reason: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def normalized_destination(self) -> Optional[str]:
        return _clean(self.destination)

    def normalized_reason(self) -> Optional[str]:
        return _clean(self.reason)

    def normalized_attributes(self) -> Dict[str, str]:
        return normalize_attributes(self.attributes)


@dataclass(frozen=True)
class MessageRecord:
    message_id: str
    payload: str
    attributes: Dict[str, str] = field(default_factory=dict)
    status: Optional[str] = None

    @classmethod
    def from_message(cls, message_id: Any, payload: Any, attributes: Optional[Mapping[str, Any]] = None, status: Any = None) -> "MessageRecord":
        return cls(
            message_id=str(message_id),
            payload=normalize_text_payload(payload),
            attributes=normalize_attributes(attributes),
            status=_clean(None if status is None else str(status)),
        )


@dataclass(frozen=True)
class MessageSummary:
    total: int = 0
    processed: int = 0
    failed: int = 0
    dead_lettered: int = 0

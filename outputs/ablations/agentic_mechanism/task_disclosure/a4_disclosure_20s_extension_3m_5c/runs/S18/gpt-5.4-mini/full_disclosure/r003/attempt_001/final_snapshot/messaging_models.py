from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union


JsonScalar = Union[str, int, float, bool, None]
JsonValue = Union[JsonScalar, Dict[str, Any], List[Any]]


def _stringify_mapping(values: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not values:
        return {}
    return {str(key): str(value) for key, value in values.items() if value is not None}


def normalize_payload_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, (bytes, bytearray)):
        return bytes(payload).decode("utf-8")
    if isinstance(payload, (dict, list, tuple)):
        import json

        return json.dumps(payload, separators=(",", ":"), sort_keys=True)
    return str(payload)


def normalize_message_data(data: Any) -> bytes:
    text = normalize_payload_text(data)
    return text.encode("utf-8")


def normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    return _stringify_mapping(attributes)


def normalize_message(message: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(message)
    if "data" in normalized:
        normalized["data"] = normalize_message_data(normalized["data"])
    if "attributes" in normalized:
        normalized["attributes"] = normalize_attributes(normalized.get("attributes"))
    if "ordering_key" in normalized and normalized["ordering_key"] is not None:
        normalized["ordering_key"] = str(normalized["ordering_key"])
    if "message_id" in normalized and normalized["message_id"] is not None:
        normalized["message_id"] = str(normalized["message_id"])
    return normalized


@dataclass(frozen=True)
class PublishEventRequest:
    topic: str
    event: Dict[str, Any]
    project_id: Optional[str] = None


@dataclass(frozen=True)
class PublishEventResponse:
    message_id: str


@dataclass(frozen=True)
class BatchPublishMessage:
    data: Any
    attributes: Dict[str, Any] = field(default_factory=dict)
    client_token: Optional[str] = None
    message_id: Optional[str] = None
    ordering_key: Optional[str] = None

    def normalize(self) -> Dict[str, Any]:
        return normalize_message(
            {
                "data": self.data,
                "attributes": self.attributes,
                "client_token": self.client_token,
                "message_id": self.message_id,
                "ordering_key": self.ordering_key,
            }
        )


@dataclass(frozen=True)
class BatchPublishRequest:
    topic: str
    messages: Sequence[BatchPublishMessage]
    project_id: Optional[str] = None

    def normalized_messages(self) -> List[Dict[str, Any]]:
        return [message.normalize() for message in self.messages]


@dataclass(frozen=True)
class BatchPublishResult:
    message_id: str
    client_token: Optional[str] = None


@dataclass(frozen=True)
class BatchPublishResponse:
    results: Sequence[BatchPublishResult]


@dataclass(frozen=True)
class ConsumeEventRequest:
    subscription: str
    project_id: Optional[str] = None
    max_messages: int = 1


@dataclass(frozen=True)
class ConsumeEventResponse:
    messages: Sequence[Dict[str, Any]]


@dataclass(frozen=True)
class DeadLetterRequest:
    destination: str
    message: Dict[str, Any]
    project_id: Optional[str] = None


@dataclass(frozen=True)
class DeadLetterResponse:
    message_id: str


@dataclass(frozen=True)
class MessageAuditRecord:
    message_id: str
    status: str
    payload: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MessageSafetyRequest:
    text: str


@dataclass(frozen=True)
class MessageSafetyResponse:
    is_safe: bool
    labels: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class MessageSummaryRequest:
    records: Sequence[MessageAuditRecord]


@dataclass(frozen=True)
class MessageSummaryResponse:
    total: int
    succeeded: int
    failed: int


@dataclass(frozen=True)
class PayloadTranslateRequest:
    text: str
    target_language: str


@dataclass(frozen=True)
class PayloadTranslateResponse:
    translated_text: str

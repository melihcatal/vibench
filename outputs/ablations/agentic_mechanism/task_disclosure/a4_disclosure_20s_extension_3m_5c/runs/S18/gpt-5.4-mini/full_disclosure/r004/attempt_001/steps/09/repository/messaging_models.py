from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = value.strip()
    return text or None


def _normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in attributes.items():
        if key is None:
            continue
        normalized[str(key)] = "" if value is None else str(value)
    return normalized


@dataclass(frozen=True)
class PublishRequest:
    topic_id: Optional[str] = None
    data: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: Optional[str] = None

    def normalized(self) -> "PublishRequest":
        return PublishRequest(
            topic_id=_normalize_text(self.topic_id),
            data=_normalize_text(self.data),
            attributes=_normalize_attributes(self.attributes),
            ordering_key=_normalize_text(self.ordering_key),
        )


@dataclass(frozen=True)
class PublishBatchRequest:
    topic_id: Optional[str] = None
    messages: List[PublishRequest] = field(default_factory=list)

    def normalized(self) -> "PublishBatchRequest":
        return PublishBatchRequest(
            topic_id=_normalize_text(self.topic_id),
            messages=[message.normalized() for message in self.messages],
        )


@dataclass(frozen=True)
class PublishResponse:
    message_id: str
    topic_id: Optional[str] = None
    published_at: datetime = field(default_factory=_utcnow)
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["published_at"] = self.published_at.isoformat()
        return payload


@dataclass(frozen=True)
class ConsumeRequest:
    subscription_id: Optional[str] = None
    max_messages: int = 1

    def normalized(self) -> "ConsumeRequest":
        return ConsumeRequest(
            subscription_id=_normalize_text(self.subscription_id),
            max_messages=max(1, int(self.max_messages)),
        )


@dataclass(frozen=True)
class ConsumedMessage:
    message_id: str
    data: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)
    publish_time: Optional[datetime] = None
    ack_id: Optional[str] = None

    def normalized(self) -> "ConsumedMessage":
        return ConsumedMessage(
            message_id=str(self.message_id),
            data=_normalize_text(self.data),
            attributes=_normalize_attributes(self.attributes),
            publish_time=self.publish_time,
            ack_id=_normalize_text(self.ack_id),
        )


@dataclass(frozen=True)
class DeadLetterRequest:
    destination: Optional[str] = None
    original_message_id: Optional[str] = None
    reason: Optional[str] = None
    data: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)

    def normalized(self) -> "DeadLetterRequest":
        return DeadLetterRequest(
            destination=_normalize_text(self.destination),
            original_message_id=_normalize_text(self.original_message_id),
            reason=_normalize_text(self.reason),
            data=_normalize_text(self.data),
            attributes=_normalize_attributes(self.attributes),
        )


@dataclass(frozen=True)
class MessageAuditRecord:
    message_id: str
    status: str
    checked_at: datetime = field(default_factory=_utcnow)
    metadata: Dict[str, str] = field(default_factory=dict)

    def normalized(self) -> "MessageAuditRecord":
        return MessageAuditRecord(
            message_id=str(self.message_id),
            status=_normalize_text(self.status) or "",
            checked_at=self.checked_at,
            metadata=_normalize_attributes(self.metadata),
        )


@dataclass(frozen=True)
class MessageSafetyRequest:
    text: Optional[str] = None
    locale: Optional[str] = None

    def normalized(self) -> "MessageSafetyRequest":
        return MessageSafetyRequest(
            text=_normalize_text(self.text),
            locale=_normalize_text(self.locale),
        )


@dataclass(frozen=True)
class MessageSummary:
    total: int
    succeeded: int
    failed: int
    details: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "MessageSummary":
        return MessageSummary(
            total=max(0, int(self.total)),
            succeeded=max(0, int(self.succeeded)),
            failed=max(0, int(self.failed)),
            details=dict(self.details),
        )


@dataclass(frozen=True)
class PayloadTranslateRequest:
    text: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None

    def normalized(self) -> "PayloadTranslateRequest":
        return PayloadTranslateRequest(
            text=_normalize_text(self.text),
            source_language=_normalize_text(self.source_language),
            target_language=_normalize_text(self.target_language),
        )


def normalize_message_batch(messages: Iterable[Mapping[str, Any]]) -> List[PublishRequest]:
    normalized: List[PublishRequest] = []
    for message in messages:
        normalized.append(
            PublishRequest(
                topic_id=message.get("topic_id"),
                data=message.get("data"),
                attributes=message.get("attributes") or {},
                ordering_key=message.get("ordering_key"),
            ).normalized()
        )
    return normalized

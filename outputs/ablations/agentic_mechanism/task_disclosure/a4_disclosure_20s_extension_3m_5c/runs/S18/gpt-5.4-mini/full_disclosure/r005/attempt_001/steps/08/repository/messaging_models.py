from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping, Optional, Sequence


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _coerce_attributes(attributes: Mapping[str, Any] | None) -> dict[str, str]:
    if not attributes:
        return {}
    return {str(key): _coerce_text(value) for key, value in attributes.items()}


def _coerce_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        text = value.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


@dataclass(frozen=True)
class MessageRecord:
    message_id: str
    data: str = ""
    attributes: dict[str, str] = field(default_factory=dict)
    publish_time: Optional[datetime] = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "MessageRecord":
        return cls(
            message_id=_coerce_text(value.get("message_id") or value.get("id") or ""),
            data=_coerce_text(value.get("data")),
            attributes=_coerce_attributes(value.get("attributes")),
            publish_time=_coerce_datetime(value.get("publish_time")),
        )

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        if self.publish_time is not None:
            result["publish_time"] = self.publish_time.isoformat()
        return result


@dataclass(frozen=True)
class PublishRequest:
    topic_path: str
    data: Any
    attributes: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "PublishRequest":
        return cls(
            topic_path=_coerce_text(value.get("topic_path") or value.get("topic") or ""),
            data=value.get("data"),
            attributes=_coerce_attributes(value.get("attributes")),
        )


@dataclass(frozen=True)
class PublishResponse:
    topic_path: str
    message_ids: list[str] = field(default_factory=list)
    provider: str = "google_cloud_pubsub"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConsumeRequest:
    subscription_path: str
    max_messages: int = 1

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ConsumeRequest":
        return cls(
            subscription_path=_coerce_text(value.get("subscription_path") or value.get("subscription") or ""),
            max_messages=int(value.get("max_messages") or 1),
        )


@dataclass(frozen=True)
class ConsumeResponse:
    subscription_path: str
    message: Optional[MessageRecord] = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.message is not None:
            payload["message"] = self.message.to_dict()
        return payload


@dataclass(frozen=True)
class DeadLetterRequest:
    destination: str
    message: MessageRecord

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "DeadLetterRequest":
        return cls(
            destination=_coerce_text(value.get("destination") or value.get("dead_letter_destination") or ""),
            message=MessageRecord.from_mapping(value.get("message") or {}),
        )


@dataclass(frozen=True)
class MessageSummary:
    total: int = 0
    succeeded: int = 0
    failed: int = 0
    skipped: int = 0

    @classmethod
    def from_results(cls, results: Sequence[Mapping[str, Any]]) -> "MessageSummary":
        total = len(results)
        succeeded = sum(1 for item in results if item.get("status") == "succeeded")
        failed = sum(1 for item in results if item.get("status") == "failed")
        skipped = sum(1 for item in results if item.get("status") == "skipped")
        return cls(total=total, succeeded=succeeded, failed=failed, skipped=skipped)


@dataclass(frozen=True)
class NormalizedMessage:
    record: MessageRecord
    normalized_text: str
    normalized_attributes: dict[str, str] = field(default_factory=dict)
    normalized_at: datetime = field(default_factory=_utc_now)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "NormalizedMessage":
        record = MessageRecord.from_mapping(value)
        text = _coerce_text(record.data).strip()
        return cls(record=record, normalized_text=text, normalized_attributes=dict(record.attributes))

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "record": self.record.to_dict(),
            "normalized_text": self.normalized_text,
            "normalized_attributes": dict(self.normalized_attributes),
            "normalized_at": self.normalized_at.isoformat(),
        }
        return payload


def normalize_message(value: Mapping[str, Any]) -> NormalizedMessage:
    return NormalizedMessage.from_mapping(value)


__all__ = [
    "ConsumeRequest",
    "ConsumeResponse",
    "DeadLetterRequest",
    "MessageRecord",
    "MessageSummary",
    "NormalizedMessage",
    "PublishRequest",
    "PublishResponse",
    "normalize_message",
]

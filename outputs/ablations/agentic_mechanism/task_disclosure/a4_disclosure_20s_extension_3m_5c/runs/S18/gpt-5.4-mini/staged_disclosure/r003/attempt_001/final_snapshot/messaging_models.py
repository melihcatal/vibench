from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_attrs(attributes: Mapping[str, Any] | None) -> dict[str, str]:
    if not attributes:
        return {}
    normalized: dict[str, str] = {}
    for key, value in attributes.items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def _normalize_data(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, memoryview):
        return data.tobytes()
    if isinstance(data, str):
        return data.encode("utf-8")
    return str(data).encode("utf-8")


@dataclass(slots=True)
class PublishRequest:
    topic: str
    data: bytes | str | bytearray | memoryview | None = None
    attributes: dict[str, str] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: uuid4().hex)
    ordering_key: str | None = None
    timestamp: datetime = field(default_factory=_utcnow)

    def normalized(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "data": _normalize_data(self.data),
            "attributes": _normalize_attrs(self.attributes),
            "message_id": self.message_id,
            "ordering_key": self.ordering_key,
            "timestamp": self.timestamp.astimezone(timezone.utc),
        }


@dataclass(slots=True)
class PublishResponse:
    topic: str
    message_id: str
    published_at: datetime = field(default_factory=_utcnow)
    attributes: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_request(cls, request: PublishRequest) -> PublishResponse:
        normalized = request.normalized()
        return cls(
            topic=normalized["topic"],
            message_id=normalized["message_id"],
            published_at=normalized["timestamp"],
            attributes=normalized["attributes"],
        )

    def normalized(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "message_id": self.message_id,
            "published_at": self.published_at.astimezone(timezone.utc),
            "attributes": _normalize_attrs(self.attributes),
        }


@dataclass(slots=True)
class SubscriptionRequest:
    subscription: str
    max_messages: int = 1
    return_immediately: bool = False
    deadline_seconds: int = 10

    def normalized(self) -> dict[str, Any]:
        return {
            "subscription": self.subscription,
            "max_messages": max(1, int(self.max_messages)),
            "return_immediately": bool(self.return_immediately),
            "deadline_seconds": max(1, int(self.deadline_seconds)),
        }


@dataclass(slots=True)
class ReceivedMessage:
    message_id: str
    data: bytes
    attributes: dict[str, str] = field(default_factory=dict)
    publish_time: datetime = field(default_factory=_utcnow)
    ordering_key: str | None = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> ReceivedMessage:
        return cls(
            message_id=str(payload.get("message_id", uuid4().hex)),
            data=_normalize_data(payload.get("data")),
            attributes=_normalize_attrs(payload.get("attributes")),
            publish_time=(payload.get("publish_time") or _utcnow()).astimezone(timezone.utc)
            if isinstance(payload.get("publish_time"), datetime)
            else _utcnow(),
            ordering_key=payload.get("ordering_key") or None,
        )

    def normalized(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "data": self.data,
            "attributes": _normalize_attrs(self.attributes),
            "publish_time": self.publish_time.astimezone(timezone.utc),
            "ordering_key": self.ordering_key,
        }


@dataclass(slots=True)
class AckRequest:
    subscription: str
    ack_ids: list[str]

    def normalized(self) -> dict[str, Any]:
        return {
            "subscription": self.subscription,
            "ack_ids": [str(ack_id) for ack_id in self.ack_ids if ack_id],
        }


@dataclass(slots=True)
class AckResponse:
    subscription: str
    acked_ids: list[str]
    failed_ids: list[str] = field(default_factory=list)

    def normalized(self) -> dict[str, Any]:
        return {
            "subscription": self.subscription,
            "acked_ids": [str(ack_id) for ack_id in self.acked_ids],
            "failed_ids": [str(ack_id) for ack_id in self.failed_ids],
        }


def normalize_publish_request(topic: str, data: Any, attributes: Mapping[str, Any] | None = None) -> PublishRequest:
    return PublishRequest(topic=topic, data=data, attributes=_normalize_attrs(attributes))


def normalize_received_message(payload: Mapping[str, Any]) -> ReceivedMessage:
    return ReceivedMessage.from_payload(payload)

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping, Optional
import base64
import json


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _dt_to_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return _ensure_utc(dt).isoformat().replace("+00:00", "Z")


def _parse_dt(value: Any) -> Optional[datetime]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return _ensure_utc(value)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        normalized = value.replace("Z", "+00:00")
        return _ensure_utc(datetime.fromisoformat(normalized))
    raise TypeError(f"Unsupported datetime value: {type(value)!r}")


def _normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> dict[str, str]:
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items()}


def _normalize_data(data: Any) -> str:
    if data is None:
        return ""
    if isinstance(data, bytes):
        return base64.b64encode(data).decode("ascii")
    if isinstance(data, str):
        return data
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def _maybe_decode_data(data: Any) -> Any:
    if data is None:
        return None
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        try:
            return base64.b64decode(data, validate=True)
        except Exception:
            return data
    return data


@dataclass(slots=True)
class PublishRequest:
    topic: str
    data: Any
    attributes: MutableMapping[str, Any] = field(default_factory=dict)
    ordering_key: Optional[str] = None

    def normalize(self) -> dict[str, Any]:
        payload = {"topic": self.topic, "data": _normalize_data(self.data)}
        attrs = _normalize_attributes(self.attributes)
        if attrs:
            payload["attributes"] = attrs
        if self.ordering_key:
            payload["orderingKey"] = self.ordering_key
        return payload


@dataclass(slots=True)
class PublishResponse:
    message_ids: list[str]
    success: bool = True
    received_at: datetime = field(default_factory=_utc_now)

    @classmethod
    def from_api(cls, payload: Mapping[str, Any]) -> "PublishResponse":
        message_ids = [str(item) for item in payload.get("messageIds", payload.get("message_ids", []))]
        success = bool(payload.get("success", True))
        received_at = _parse_dt(payload.get("receivedAt", payload.get("received_at"))) or _utc_now()
        return cls(message_ids=message_ids, success=success, received_at=received_at)

    def normalize(self) -> dict[str, Any]:
        return {
            "messageIds": list(self.message_ids),
            "success": self.success,
            "receivedAt": _dt_to_iso(self.received_at),
        }


@dataclass(slots=True)
class SubscriptionMessage:
    message_id: str
    data: Any
    attributes: dict[str, str] = field(default_factory=dict)
    publish_time: Optional[datetime] = None
    ordering_key: Optional[str] = None

    @classmethod
    def from_api(cls, payload: Mapping[str, Any]) -> "SubscriptionMessage":
        return cls(
            message_id=str(payload.get("messageId", payload.get("message_id", ""))),
            data=_maybe_decode_data(payload.get("data")),
            attributes={str(k): str(v) for k, v in dict(payload.get("attributes", {})).items()},
            publish_time=_parse_dt(payload.get("publishTime", payload.get("publish_time"))),
            ordering_key=payload.get("orderingKey", payload.get("ordering_key")),
        )

    def normalize(self) -> dict[str, Any]:
        payload = {
            "messageId": self.message_id,
            "data": _normalize_data(self.data),
            "attributes": dict(self.attributes),
        }
        if self.publish_time is not None:
            payload["publishTime"] = _dt_to_iso(self.publish_time)
        if self.ordering_key:
            payload["orderingKey"] = self.ordering_key
        return payload


@dataclass(slots=True)
class PullRequest:
    subscription: str
    max_messages: int = 1
    return_immediately: bool = False

    def normalize(self) -> dict[str, Any]:
        return {
            "subscription": self.subscription,
            "maxMessages": int(self.max_messages),
            "returnImmediately": bool(self.return_immediately),
        }


@dataclass(slots=True)
class PullResponse:
    received_messages: list[SubscriptionMessage] = field(default_factory=list)

    @classmethod
    def from_api(cls, payload: Mapping[str, Any]) -> "PullResponse":
        messages = payload.get("receivedMessages", payload.get("received_messages", []))
        return cls(received_messages=[SubscriptionMessage.from_api(item) for item in messages])

    def normalize(self) -> dict[str, Any]:
        return {"receivedMessages": [message.normalize() for message in self.received_messages]}

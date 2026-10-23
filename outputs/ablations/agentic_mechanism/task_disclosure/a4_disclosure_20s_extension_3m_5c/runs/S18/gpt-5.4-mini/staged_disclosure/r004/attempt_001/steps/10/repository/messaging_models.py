from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence, Union


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _to_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _normalize_headers(headers: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not headers:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in headers.items():
        normalized[_to_str(key)] = _to_str(value)
    return normalized


def _normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    return _normalize_headers(attributes)


def _normalize_payload(payload: Any) -> Union[str, bytes, Dict[str, Any], List[Any], None]:
    if payload is None:
        return None
    if isinstance(payload, (str, bytes, dict, list)):
        return payload
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    if hasattr(payload, "dict"):
        return payload.dict()
    return payload


@dataclass(frozen=True)
class PublishMessageRequest:
    topic: str
    data: Union[str, bytes, Dict[str, Any], List[Any], None]
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None
    ordering_key: Optional[str] = None
    publish_time: Optional[str] = None

    @classmethod
    def from_raw(cls, topic: str, payload: Any, attributes: Optional[Mapping[str, Any]] = None, **kwargs: Any) -> "PublishMessageRequest":
        return cls(
            topic=_to_str(topic),
            data=_normalize_payload(payload),
            attributes=_normalize_attributes(attributes),
            message_id=_to_str(kwargs.get("message_id")) or None,
            ordering_key=_to_str(kwargs.get("ordering_key")) or None,
            publish_time=_to_str(kwargs.get("publish_time")) or None,
        )

    def with_publish_time(self, publish_time: Optional[str] = None) -> "PublishMessageRequest":
        return PublishMessageRequest(
            topic=self.topic,
            data=self.data,
            attributes=dict(self.attributes),
            message_id=self.message_id,
            ordering_key=self.ordering_key,
            publish_time=publish_time or _now_utc_iso(),
        )


@dataclass(frozen=True)
class PublishMessageResponse:
    topic: str
    message_id: str
    publish_time: str
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any]) -> "PublishMessageResponse":
        topic = _to_str(raw.get("topic") or raw.get("topic_name") or raw.get("name"))
        message_id = _to_str(raw.get("message_id") or raw.get("id") or raw.get("messageId"))
        publish_time = _to_str(raw.get("publish_time") or raw.get("publishTime") or raw.get("timestamp") or _now_utc_iso())
        attributes = _normalize_attributes(raw.get("attributes") if isinstance(raw.get("attributes"), Mapping) else None)
        ordering_key = raw.get("ordering_key") or raw.get("orderingKey")
        return cls(
            topic=topic,
            message_id=message_id,
            publish_time=publish_time,
            attributes=attributes,
            ordering_key=_to_str(ordering_key) or None,
            raw=dict(raw),
        )


@dataclass(frozen=True)
class SubscriptionRequest:
    topic: str
    subscription: str
    filter: Optional[str] = None
    ack_deadline_seconds: Optional[int] = None
    retain_acked_messages: bool = False
    expiration_policy: Optional[Dict[str, Any]] = None

    @classmethod
    def from_raw(cls, topic: str, subscription: str, **kwargs: Any) -> "SubscriptionRequest":
        return cls(
            topic=_to_str(topic),
            subscription=_to_str(subscription),
            filter=_to_str(kwargs.get("filter")) or None,
            ack_deadline_seconds=kwargs.get("ack_deadline_seconds"),
            retain_acked_messages=bool(kwargs.get("retain_acked_messages", False)),
            expiration_policy=kwargs.get("expiration_policy"),
        )


@dataclass(frozen=True)
class SubscriptionResponse:
    topic: str
    subscription: str
    state: str
    message_count: int = 0
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any]) -> "SubscriptionResponse":
        return cls(
            topic=_to_str(raw.get("topic") or raw.get("topic_name")),
            subscription=_to_str(raw.get("subscription") or raw.get("name") or raw.get("subscription_name")),
            state=_to_str(raw.get("state") or raw.get("status") or "unknown"),
            message_count=int(raw.get("message_count") or raw.get("messages") or 0),
            raw=dict(raw),
        )


def normalize_message(message: Any) -> Dict[str, Any]:
    if isinstance(message, Mapping):
        return {
            "topic": _to_str(message.get("topic") or message.get("topic_name")),
            "message_id": _to_str(message.get("message_id") or message.get("id") or message.get("messageId")),
            "publish_time": _to_str(message.get("publish_time") or message.get("publishTime") or _now_utc_iso()),
            "data": _normalize_payload(message.get("data")),
            "attributes": _normalize_attributes(message.get("attributes") if isinstance(message.get("attributes"), Mapping) else None),
            "ordering_key": _to_str(message.get("ordering_key") or message.get("orderingKey")) or None,
        }
    return {
        "topic": "",
        "message_id": "",
        "publish_time": _now_utc_iso(),
        "data": _normalize_payload(message),
        "attributes": {},
        "ordering_key": None,
    }


def normalize_messages(messages: Sequence[Any]) -> List[Dict[str, Any]]:
    return [normalize_message(message) for message in messages]


def normalize_subscription(subscription: Any) -> Dict[str, Any]:
    if isinstance(subscription, Mapping):
        return {
            "topic": _to_str(subscription.get("topic") or subscription.get("topic_name")),
            "subscription": _to_str(subscription.get("subscription") or subscription.get("name") or subscription.get("subscription_name")),
            "state": _to_str(subscription.get("state") or subscription.get("status") or "unknown"),
            "message_count": int(subscription.get("message_count") or subscription.get("messages") or 0),
        }
    return {"topic": "", "subscription": _to_str(subscription), "state": "unknown", "message_count": 0}

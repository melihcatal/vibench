from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional
import base64


def _coerce_str_map(value: Optional[Mapping[Any, Any]]) -> Dict[str, str]:
    if not value:
        return {}
    return {str(k): str(v) for k, v in value.items()}


def _coerce_bytes(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, (dict, list, tuple, set)):
        import json

        return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return str(data).encode("utf-8")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PubSubMessageRequest:
    data: bytes = b""
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: str = ""

    @classmethod
    def from_payload(
        cls,
        payload: Any,
        attributes: Optional[Mapping[Any, Any]] = None,
        ordering_key: str = "",
    ) -> "PubSubMessageRequest":
        return cls(
            data=_coerce_bytes(payload),
            attributes=_coerce_str_map(attributes),
            ordering_key=str(ordering_key or ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": base64.b64encode(self.data).decode("ascii"),
            "attributes": dict(self.attributes),
            "ordering_key": self.ordering_key,
        }


@dataclass(frozen=True)
class PubSubPublishRequest:
    topic: str
    messages: list[PubSubMessageRequest]

    @classmethod
    def from_single(
        cls,
        topic: str,
        payload: Any,
        attributes: Optional[Mapping[Any, Any]] = None,
        ordering_key: str = "",
    ) -> "PubSubPublishRequest":
        return cls(topic=topic, messages=[PubSubMessageRequest.from_payload(payload, attributes, ordering_key)])


@dataclass(frozen=True)
class PubSubPublishResponse:
    message_ids: list[str]
    topic: str

    def normalized(self) -> Dict[str, Any]:
        return {"topic": self.topic, "message_ids": list(self.message_ids)}


@dataclass(frozen=True)
class PubSubReceivedMessage:
    ack_id: str
    data: bytes
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: str = ""
    publish_time: str = ""
    ordering_key: str = ""

    @classmethod
    def from_pubsub(cls, received_message: Any) -> "PubSubReceivedMessage":
        message = getattr(received_message, "message", None)
        data = getattr(message, "data", b"") if message is not None else b""
        attributes = getattr(message, "attributes", {}) if message is not None else {}
        publish_time = getattr(message, "publish_time", None) if message is not None else None
        if publish_time is None:
            publish_time_str = _utc_now_iso()
        elif hasattr(publish_time, "isoformat"):
            publish_time_str = publish_time.isoformat()
        else:
            publish_time_str = str(publish_time)
        return cls(
            ack_id=str(getattr(received_message, "ack_id", "")),
            data=_coerce_bytes(data),
            attributes=_coerce_str_map(attributes),
            message_id=str(getattr(message, "message_id", "")) if message is not None else "",
            publish_time=publish_time_str,
            ordering_key=str(getattr(message, "ordering_key", "")) if message is not None else "",
        )

    def decoded_data(self) -> str:
        return self.data.decode("utf-8", errors="replace")

    def normalized(self) -> Dict[str, Any]:
        return {
            "ack_id": self.ack_id,
            "data": self.decoded_data(),
            "attributes": dict(self.attributes),
            "message_id": self.message_id,
            "publish_time": self.publish_time,
            "ordering_key": self.ordering_key,
        }


@dataclass(frozen=True)
class PubSubPullResponse:
    messages: list[PubSubReceivedMessage]

    @classmethod
    def from_pubsub(cls, response: Any) -> "PubSubPullResponse":
        received = getattr(response, "received_messages", []) or []
        return cls(messages=[PubSubReceivedMessage.from_pubsub(msg) for msg in received])

    def normalized(self) -> Dict[str, Any]:
        return {"messages": [message.normalized() for message in self.messages]}


def normalize_message_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, PubSubReceivedMessage):
        return payload.normalized()
    if isinstance(payload, PubSubMessageRequest):
        return payload.to_dict()
    if isinstance(payload, bytes):
        return {"data": payload.decode("utf-8", errors="replace")}
    if isinstance(payload, str):
        return {"data": payload}
    if isinstance(payload, Mapping):
        return {str(k): v for k, v in payload.items()}
    return {"data": str(payload)}

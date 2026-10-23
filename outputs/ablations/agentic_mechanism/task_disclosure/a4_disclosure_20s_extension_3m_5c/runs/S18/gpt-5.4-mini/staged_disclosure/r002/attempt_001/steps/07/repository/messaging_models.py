from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Union


def _normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in attributes.items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def _normalize_data(data: Union[str, bytes, bytearray, None]) -> Optional[bytes]:
    if data is None:
        return None
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    return str(data).encode("utf-8")


def _normalize_messages(messages: Optional[Iterable[Mapping[str, Any]]]) -> List[Dict[str, Any]]:
    if not messages:
        return []
    normalized: List[Dict[str, Any]] = []
    for message in messages:
        normalized.append(normalize_pubsub_message_request(message))
    return normalized


def normalize_pubsub_message_request(message: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    if "data" in message:
        data = _normalize_data(message.get("data"))
        if data is not None:
            normalized["data"] = data
    if "attributes" in message:
        normalized["attributes"] = _normalize_attributes(message.get("attributes"))
    if "ordering_key" in message and message.get("ordering_key") is not None:
        normalized["ordering_key"] = str(message.get("ordering_key"))
    if "message_id" in message and message.get("message_id") is not None:
        normalized["message_id"] = str(message.get("message_id"))
    if "publish_time" in message and message.get("publish_time") is not None:
        normalized["publish_time"] = str(message.get("publish_time"))
    if "ack_id" in message and message.get("ack_id") is not None:
        normalized["ack_id"] = str(message.get("ack_id"))
    return normalized


@dataclass(frozen=True)
class PublishRequest:
    topic: str
    messages: List[Dict[str, Any]] = field(default_factory=list)

    def normalized(self) -> Dict[str, Any]:
        return {"topic": str(self.topic), "messages": _normalize_messages(self.messages)}


@dataclass(frozen=True)
class PublishResponse:
    message_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, payload: Mapping[str, Any]) -> "PublishResponse":
        message_ids = payload.get("messageIds") or payload.get("message_ids") or []
        return cls(message_ids=[str(message_id) for message_id in message_ids])


@dataclass(frozen=True)
class PullRequest:
    subscription: str
    max_messages: int = 1
    return_immediately: bool = False

    def normalized(self) -> Dict[str, Any]:
        return {
            "subscription": str(self.subscription),
            "maxMessages": int(self.max_messages),
            "returnImmediately": bool(self.return_immediately),
        }


@dataclass(frozen=True)
class ReceivedMessage:
    ack_id: str
    message: Dict[str, Any]

    @classmethod
    def from_api_response(cls, payload: Mapping[str, Any]) -> "ReceivedMessage":
        message = payload.get("message") or {}
        return cls(
            ack_id=str(payload.get("ackId", payload.get("ack_id", ""))),
            message=normalize_pubsub_message_request(message),
        )


@dataclass(frozen=True)
class PullResponse:
    received_messages: List[ReceivedMessage] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, payload: Mapping[str, Any]) -> "PullResponse":
        raw_messages = payload.get("receivedMessages") or payload.get("received_messages") or []
        return cls(received_messages=[ReceivedMessage.from_api_response(item) for item in raw_messages])


@dataclass(frozen=True)
class AcknowledgeRequest:
    subscription: str
    ack_ids: List[str] = field(default_factory=list)

    def normalized(self) -> Dict[str, Any]:
        return {"subscription": str(self.subscription), "ackIds": [str(ack_id) for ack_id in self.ack_ids]}


@dataclass(frozen=True)
class ModifyAckDeadlineRequest:
    subscription: str
    ack_ids: List[str] = field(default_factory=list)
    ack_deadline_seconds: int = 0

    def normalized(self) -> Dict[str, Any]:
        return {
            "subscription": str(self.subscription),
            "ackIds": [str(ack_id) for ack_id in self.ack_ids],
            "ackDeadlineSeconds": int(self.ack_deadline_seconds),
        }


@dataclass(frozen=True)
class SubscriptionMessage:
    subscription: str
    received_message: ReceivedMessage

    @property
    def ack_id(self) -> str:
        return self.received_message.ack_id

    @property
    def message(self) -> Dict[str, Any]:
        return self.received_message.message

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union


JsonDict = Dict[str, Any]


def _coerce_str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        return [str(item) for item in value if item is not None]
    return [str(value)]


def _coerce_dict(value: Any) -> JsonDict:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    return {}


@dataclass
class PublishRequest:
    topic: str
    messages: List[JsonDict] = field(default_factory=list)
    validate_only: bool = False

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PublishRequest":
        return cls(
            topic=str(payload.get("topic", "")),
            messages=[_coerce_dict(message) for message in payload.get("messages", []) or []],
            validate_only=bool(payload.get("validate_only", False)),
        )

    def to_dict(self) -> JsonDict:
        return {
            "topic": self.topic,
            "messages": [dict(message) for message in self.messages],
            "validate_only": self.validate_only,
        }


@dataclass
class AcknowledgeRequest:
    subscription: str
    ack_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "AcknowledgeRequest":
        return cls(
            subscription=str(payload.get("subscription", "")),
            ack_ids=_coerce_str_list(payload.get("ack_ids", [])),
        )

    def to_dict(self) -> JsonDict:
        return {"subscription": self.subscription, "ack_ids": list(self.ack_ids)}


@dataclass
class PullRequest:
    subscription: str
    max_messages: int = 1

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PullRequest":
        return cls(
            subscription=str(payload.get("subscription", "")),
            max_messages=int(payload.get("max_messages", 1) or 1),
        )

    def to_dict(self) -> JsonDict:
        return {"subscription": self.subscription, "max_messages": self.max_messages}


@dataclass
class MessagePayload:
    data: str = ""
    attributes: JsonDict = field(default_factory=dict)
    message_id: str = ""
    publish_time: str = ""
    ordering_key: str = ""

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "MessagePayload":
        return cls(
            data=str(payload.get("data", "")),
            attributes=_coerce_dict(payload.get("attributes", {})),
            message_id=str(payload.get("message_id", payload.get("messageId", ""))),
            publish_time=str(payload.get("publish_time", payload.get("publishTime", ""))),
            ordering_key=str(payload.get("ordering_key", payload.get("orderingKey", ""))),
        )

    def to_dict(self) -> JsonDict:
        return {
            "data": self.data,
            "attributes": dict(self.attributes),
            "message_id": self.message_id,
            "publish_time": self.publish_time,
            "ordering_key": self.ordering_key,
        }


@dataclass
class PublishResponse:
    message_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PublishResponse":
        return cls(message_ids=_coerce_str_list(payload.get("message_ids", payload.get("messageIds", []))))

    def to_dict(self) -> JsonDict:
        return {"message_ids": list(self.message_ids)}


@dataclass
class PullResponse:
    received_messages: List[MessagePayload] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PullResponse":
        messages = payload.get("received_messages", payload.get("receivedMessages", [])) or []
        return cls(received_messages=[MessagePayload.from_dict(message) for message in messages])

    def to_dict(self) -> JsonDict:
        return {"received_messages": [message.to_dict() for message in self.received_messages]}


def normalize_publish_request(payload: Union[PublishRequest, Mapping[str, Any]]) -> JsonDict:
    return payload.to_dict() if isinstance(payload, PublishRequest) else PublishRequest.from_dict(payload).to_dict()


def normalize_acknowledge_request(payload: Union[AcknowledgeRequest, Mapping[str, Any]]) -> JsonDict:
    return payload.to_dict() if isinstance(payload, AcknowledgeRequest) else AcknowledgeRequest.from_dict(payload).to_dict()


def normalize_pull_request(payload: Union[PullRequest, Mapping[str, Any]]) -> JsonDict:
    return payload.to_dict() if isinstance(payload, PullRequest) else PullRequest.from_dict(payload).to_dict()


def normalize_publish_response(payload: Union[PublishResponse, Mapping[str, Any]]) -> JsonDict:
    return payload.to_dict() if isinstance(payload, PublishResponse) else PublishResponse.from_dict(payload).to_dict()


def normalize_pull_response(payload: Union[PullResponse, Mapping[str, Any]]) -> JsonDict:
    return payload.to_dict() if isinstance(payload, PullResponse) else PullResponse.from_dict(payload).to_dict()

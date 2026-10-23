from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


def _clean_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").strip()
    return str(value).strip()


def _clean_mapping(value: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not value:
        return {}
    return {str(k): _clean_str(v) for k, v in value.items() if _clean_str(v) != ""}


def _clean_list(value: Optional[Iterable[Any]]) -> List[str]:
    if not value:
        return []
    return [_clean_str(item) for item in value if _clean_str(item) != ""]


def normalize_message_id(message_id: Any) -> str:
    return _clean_str(message_id)


def normalize_topic_id(topic_id: Any) -> str:
    return _clean_str(topic_id)


def normalize_subscription_id(subscription_id: Any) -> str:
    return _clean_str(subscription_id)


def normalize_payload_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, (dict, list)):
        return _clean_str(payload)
    if isinstance(payload, bytes):
        return payload.decode("utf-8", errors="replace")
    return _clean_str(payload)


def normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    return _clean_mapping(attributes)


def normalize_message_record(record: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = dict(record)
    if "message_id" in normalized:
        normalized["message_id"] = normalize_message_id(normalized.get("message_id"))
    if "topic_id" in normalized:
        normalized["topic_id"] = normalize_topic_id(normalized.get("topic_id"))
    if "subscription_id" in normalized:
        normalized["subscription_id"] = normalize_subscription_id(normalized.get("subscription_id"))
    if "payload_text" in normalized:
        normalized["payload_text"] = normalize_payload_text(normalized.get("payload_text"))
    if "attributes" in normalized:
        normalized["attributes"] = normalize_attributes(normalized.get("attributes"))
    if "tags" in normalized:
        normalized["tags"] = _clean_list(normalized.get("tags"))
    return normalized


@dataclass(frozen=True)
class MessageRequest:
    message_id: str = ""
    topic_id: str = ""
    subscription_id: str = ""
    payload_text: str = ""
    attributes: Dict[str, str] = field(default_factory=dict)

    def normalized(self) -> "MessageRequest":
        return MessageRequest(
            message_id=normalize_message_id(self.message_id),
            topic_id=normalize_topic_id(self.topic_id),
            subscription_id=normalize_subscription_id(self.subscription_id),
            payload_text=normalize_payload_text(self.payload_text),
            attributes=normalize_attributes(self.attributes),
        )


@dataclass(frozen=True)
class MessageResponse:
    ok: bool = False
    message_id: str = ""
    status: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "MessageResponse":
        details = dict(self.details)
        if "message_id" in details:
            details["message_id"] = normalize_message_id(details.get("message_id"))
        if "status" in details:
            details["status"] = _clean_str(details.get("status"))
        return MessageResponse(
            ok=bool(self.ok),
            message_id=normalize_message_id(self.message_id),
            status=_clean_str(self.status),
            details=details,
        )


@dataclass(frozen=True)
class BatchRequest:
    topic_id: str = ""
    messages: List[MessageRequest] = field(default_factory=list)

    def normalized(self) -> "BatchRequest":
        return BatchRequest(
            topic_id=normalize_topic_id(self.topic_id),
            messages=[message.normalized() for message in self.messages],
        )


@dataclass(frozen=True)
class BatchResponse:
    ok: bool = False
    published_ids: List[str] = field(default_factory=list)
    failed_ids: List[str] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)

    def normalized(self) -> "BatchResponse":
        return BatchResponse(
            ok=bool(self.ok),
            published_ids=_clean_list(self.published_ids),
            failed_ids=_clean_list(self.failed_ids),
            errors=[normalize_message_record(error) for error in self.errors],
        )


def as_message_request(data: Mapping[str, Any]) -> MessageRequest:
    return MessageRequest(
        message_id=_clean_str(data.get("message_id", "")),
        topic_id=_clean_str(data.get("topic_id", "")),
        subscription_id=_clean_str(data.get("subscription_id", "")),
        payload_text=normalize_payload_text(data.get("payload_text", "")),
        attributes=normalize_attributes(data.get("attributes")),
    ).normalized()


def as_message_response(data: Mapping[str, Any]) -> MessageResponse:
    return MessageResponse(
        ok=bool(data.get("ok", False)),
        message_id=_clean_str(data.get("message_id", "")),
        status=_clean_str(data.get("status", "")),
        details=dict(data.get("details") or {}),
    ).normalized()


def as_batch_request(data: Mapping[str, Any]) -> BatchRequest:
    messages = [as_message_request(item) for item in data.get("messages", []) or []]
    return BatchRequest(topic_id=_clean_str(data.get("topic_id", "")), messages=messages).normalized()


def as_batch_response(data: Mapping[str, Any]) -> BatchResponse:
    return BatchResponse(
        ok=bool(data.get("ok", False)),
        published_ids=_clean_list(data.get("published_ids")),
        failed_ids=_clean_list(data.get("failed_ids")),
        errors=[normalize_message_record(item) for item in data.get("errors", []) or []],
    ).normalized()

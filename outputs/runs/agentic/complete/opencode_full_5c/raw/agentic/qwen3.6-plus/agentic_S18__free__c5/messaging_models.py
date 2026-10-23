import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class PublishRequest:
    data: Dict[str, Any]
    event_type: str = "default"
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "data": self.data,
            "event_type": self.event_type,
            "attributes": self.attributes,
        }


@dataclass
class PublishResponse:
    message_id: str
    topic_path: str
    status: str
    event_type: str = "default"
    event_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "message_id": self.message_id,
            "topic_path": self.topic_path,
            "status": self.status,
            "event_type": self.event_type,
            "event_id": self.event_id,
        }


@dataclass
class ConsumedEvent:
    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]
    publish_time: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "message_id": self.message_id,
            "data": self.data,
            "attributes": self.attributes,
            "publish_time": self.publish_time,
        }


@dataclass
class ConsumeResponse:
    event: Optional[ConsumedEvent]
    status: str
    subscription_path: str

    def to_dict(self) -> dict:
        return {
            "event": self.event.to_dict() if self.event else None,
            "status": self.status,
            "subscription_path": self.subscription_path,
        }


@dataclass
class DeadLetterRequest:
    original_message_id: str
    original_data: Dict[str, Any]
    error_reason: str
    retry_count: int = 0
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "original_message_id": self.original_message_id,
            "original_data": self.original_data,
            "error_reason": self.error_reason,
            "retry_count": self.retry_count,
            "attributes": self.attributes,
        }


@dataclass
class DeadLetterResponse:
    dlq_message_id: str
    original_message_id: str
    dlq_topic_path: str
    status: str
    error_reason: str

    def to_dict(self) -> dict:
        return {
            "dlq_message_id": self.dlq_message_id,
            "original_message_id": self.original_message_id,
            "dlq_topic_path": self.dlq_topic_path,
            "status": self.status,
            "error_reason": self.error_reason,
        }


@dataclass
class BatchPublishRequest:
    events: List[Dict[str, Any]]
    event_type: str = "batch"
    default_attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "events": self.events,
            "event_type": self.event_type,
            "default_attributes": self.default_attributes,
        }


@dataclass
class BatchPublishResponse:
    published: List[PublishResponse]
    failed: List[Dict[str, str]]
    total_requested: int
    topic_path: str

    def to_dict(self) -> dict:
        return {
            "published": [r.to_dict() for r in self.published],
            "failed": self.failed,
            "total_requested": self.total_requested,
            "total_published": len(self.published),
            "total_failed": len(self.failed),
            "topic_path": self.topic_path,
        }


def normalize_payload(raw_data: Any) -> Dict[str, Any]:
    if isinstance(raw_data, str):
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError:
            return {"raw_text": raw_data}
    if isinstance(raw_data, dict):
        return raw_data
    return {"value": raw_data}


def extract_text_from_payload(payload: Dict[str, Any]) -> str:
    text_fields = ["text", "message", "body", "content", "description"]
    for field_name in text_fields:
        if field_name in payload and isinstance(payload[field_name], str):
            return payload[field_name]
    return json.dumps(payload, ensure_ascii=False)

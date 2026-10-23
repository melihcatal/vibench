import os
import json
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class MessagingConfig:
    project_id: str = ""
    topic_id: str = ""
    subscription_id: str = ""
    dead_letter_topic_id: str = ""
    credentials_path: str = ""

    @classmethod
    def from_env(cls) -> "MessagingConfig":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT", ""),
            topic_id=os.getenv("PUBSUB_TOPIC_ID", ""),
            subscription_id=os.getenv("PUBSUB_SUBSCRIPTION_ID", ""),
            dead_letter_topic_id=os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", ""),
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""),
        )


@dataclass
class EventMessage:
    event_id: str = ""
    event_type: str = ""
    source: str = ""
    timestamp: str = ""
    payload: dict = field(default_factory=dict)
    attributes: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.event_id:
            self.event_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> "EventMessage":
        return cls(
            event_id=data.get("event_id", ""),
            event_type=data.get("event_type", ""),
            source=data.get("source", ""),
            timestamp=data.get("timestamp", ""),
            payload=data.get("payload", {}),
            attributes=data.get("attributes", {}),
        )

    @classmethod
    def from_json(cls, raw: str) -> "EventMessage":
        return cls.from_dict(json.loads(raw))


@dataclass
class PublishResult:
    message_id: str = ""
    event_id: str = ""
    status: str = ""
    timestamp: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResult:
    event: Optional[EventMessage] = None
    ack_id: str = ""
    delivery_attempt: int = 0
    status: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        if self.event:
            d["event"] = self.event.to_dict()
        return d


@dataclass
class BatchPublishResult:
    published_count: int = 0
    failed_count: int = 0
    message_ids: list = field(default_factory=list)
    errors: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DeadLetterResult:
    original_message_id: str = ""
    dead_letter_message_id: str = ""
    reason: str = ""
    status: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_payload(data: Any) -> dict:
    if isinstance(data, str):
        try:
            return json.loads(data)
        except (json.JSONDecodeError, ValueError):
            return {"raw_text": data}
    if isinstance(data, dict):
        return data
    return {"value": str(data)}


def sanitize_event_attributes(attrs: dict) -> dict:
    return {k: str(v) for k, v in attrs.items() if v is not None}

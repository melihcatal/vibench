import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class PubSubEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    source: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    payload: dict = field(default_factory=dict)
    attributes: dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, raw: str) -> "PubSubEvent":
        data = json.loads(raw)
        known_fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**known_fields)


@dataclass
class PublishResult:
    message_id: str
    event_id: str
    topic: str
    acknowledged: bool = True
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResult:
    message_id: str
    event: Optional[PubSubEvent] = None
    raw_data: Optional[str] = None
    delivery_attempt: int = 1
    acknowledged: bool = False

    def to_event(self) -> Optional[PubSubEvent]:
        if self.event:
            return self.event
        if self.raw_data:
            try:
                return PubSubEvent.from_json(self.raw_data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None


@dataclass
class DeadLetterResult:
    original_message_id: str
    dead_letter_message_id: str
    dead_letter_topic: str
    failure_reason: str
    redelivery_count: int
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BatchPublishResult:
    total_messages: int
    successful_ids: list = field(default_factory=list)
    failed_ids: list = field(default_factory=list)
    topic: str = ""

    def success_count(self) -> int:
        return len(self.successful_ids)

    def failure_count(self) -> int:
        return len(self.failed_ids)

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_payload(raw: Any) -> dict:
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
            return {"value": parsed}
        except json.JSONDecodeError:
            return {"raw_text": raw}
    if isinstance(raw, dict):
        return raw
    return {"value": str(raw)}


def normalize_attributes(attrs: Any) -> dict:
    if attrs is None:
        return {}
    if isinstance(attrs, dict):
        return {k: str(v) for k, v in attrs.items()}
    return {"source": str(attrs)}


def build_event_dict(event: PubSubEvent) -> dict:
    return {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "source": event.source,
        "timestamp": event.timestamp,
        "payload": event.payload,
        "attributes": event.attributes,
    }

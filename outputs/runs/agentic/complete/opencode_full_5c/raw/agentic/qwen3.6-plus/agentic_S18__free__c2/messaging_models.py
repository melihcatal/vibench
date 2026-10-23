import os
import json
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class PubSubEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "default"
    source: str = "unknown"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    payload: dict = field(default_factory=dict)
    attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> "PubSubEvent":
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "default"),
            source=data.get("source", "unknown"),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            payload=data.get("payload", {}),
            attributes=data.get("attributes", {}),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "PubSubEvent":
        return cls.from_dict(json.loads(json_str))


@dataclass
class PublishResult:
    message_id: str
    event_id: str
    status: str = "published"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResult:
    event: Optional[PubSubEvent] = None
    ack_id: str = ""
    status: str = "consumed"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "event": self.event.to_dict() if self.event else None,
            "ack_id": self.ack_id,
            "status": self.status,
            "timestamp": self.timestamp,
        }


@dataclass
class DeadLetterResult:
    original_message_id: str
    dead_letter_message_id: str
    failure_reason: str = ""
    retry_count: int = 0
    status: str = "dead_lettered"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BatchPublishResult:
    message_ids: list[str] = field(default_factory=list)
    event_ids: list[str] = field(default_factory=list)
    total_published: int = 0
    status: str = "batch_published"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditRecord:
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_id: str = ""
    message_id: str = ""
    processing_status: str = ""
    processing_result: dict = field(default_factory=dict)
    processed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AuditRecord":
        return cls(
            record_id=data.get("record_id", str(uuid.uuid4())),
            event_id=data.get("event_id", ""),
            message_id=data.get("message_id", ""),
            processing_status=data.get("processing_status", ""),
            processing_result=data.get("processing_result", {}),
            processed_at=data.get(
                "processed_at", datetime.now(timezone.utc).isoformat()
            ),
            metadata=data.get("metadata", {}),
        )


def normalize_payload(raw: Any) -> dict:
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {"raw_text": raw}
    if isinstance(raw, bytes):
        try:
            return json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"raw_bytes": raw.decode("utf-8", errors="replace")}
    if isinstance(raw, dict):
        return raw
    return {"value": raw}


def build_event_attributes(**kwargs: str) -> dict:
    attrs = {}
    for key, value in kwargs.items():
        if value is not None:
            attrs[key] = str(value)
    return attrs

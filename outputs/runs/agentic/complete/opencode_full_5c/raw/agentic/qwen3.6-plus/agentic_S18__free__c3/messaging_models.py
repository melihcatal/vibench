import uuid
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime, timezone


@dataclass
class EventMessage:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    source: str = ""
    payload: dict = field(default_factory=dict)
    attributes: dict = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json_bytes(self) -> bytes:
        import json

        return json.dumps(self.to_dict()).encode("utf-8")

    @classmethod
    def from_dict(cls, data: dict) -> "EventMessage":
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered)


@dataclass
class PublishResponse:
    success: bool = False
    message_id: str = ""
    event_id: str = ""
    topic: str = ""
    error: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResponse:
    success: bool = False
    event: Optional[EventMessage] = None
    ack_id: str = ""
    subscription: str = ""
    error: str = ""

    def to_dict(self) -> dict:
        result = asdict(self)
        if self.event:
            result["event"] = self.event.to_dict()
        return result


@dataclass
class BatchPublishResponse:
    success: bool = False
    message_ids: list = field(default_factory=list)
    event_ids: list = field(default_factory=list)
    total_published: int = 0
    total_failed: int = 0
    topic: str = ""
    errors: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DeadLetterResponse:
    success: bool = False
    dead_letter_id: str = ""
    original_event_id: str = ""
    destination_topic: str = ""
    failure_reason: str = ""
    retry_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditRecord:
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_id: str = ""
    event_type: str = ""
    status: str = ""
    processed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    processing_result: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_payload(data: Any) -> dict:
    if isinstance(data, dict):
        return data
    if isinstance(data, bytes):
        import json

        return json.loads(data.decode("utf-8"))
    if isinstance(data, str):
        import json

        return json.loads(data)
    return {"raw": str(data)}


def compute_payload_hash(payload: dict) -> str:
    import json

    canonical = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def sanitize_attributes(attributes: dict) -> dict:
    return {str(k): str(v)[:1024] for k, v in attributes.items() if k and v is not None}

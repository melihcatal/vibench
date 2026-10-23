from dataclasses import dataclass, field, asdict
from typing import Any
from datetime import datetime, timezone


@dataclass
class PublishRequest:
    event_type: str
    payload: dict
    attributes: dict = field(default_factory=dict)
    message_id: str | None = None
    timestamp: str | None = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        if self.message_id is None:
            self.message_id = f"evt-{id(self)}"

    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type,
            "payload": self.payload,
            "attributes": {
                "message_id": self.message_id,
                "event_type": self.event_type,
                "timestamp": self.timestamp,
                **self.attributes,
            },
        }


@dataclass
class ConsumedMessage:
    message_id: str
    data: dict
    attributes: dict
    received_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def from_raw(cls, raw: dict) -> "ConsumedMessage":
        return cls(
            message_id=raw.get("message_id", ""),
            data=raw.get("data", {}),
            attributes=raw.get("attributes", {}),
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DeadLetterRecord:
    original_message: dict
    error_reason: str
    retry_count: int = 0
    attributes: dict = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_publish_payload(self) -> dict:
        return {
            "original_message": self.original_message,
            "error_reason": self.error_reason,
            "retry_count": self.retry_count,
            "timestamp": self.timestamp,
        }


@dataclass
class BatchPublishRequest:
    events: list[PublishRequest]
    batch_id: str = field(default_factory=lambda: f"batch-{id(object())}")

    def to_items(self) -> list[dict]:
        return [e.to_dict() for e in self.events]


def normalize_event_payload(raw: Any) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, NameError):
            return {"raw": raw}
    return {"raw": str(raw)}


def extract_event_type(message: dict) -> str:
    return (
        message.get("attributes", {}).get("event_type")
        or message.get("event_type")
        or "unknown"
    )


def build_response(
    status: str, message_id: str | None = None, data: dict | None = None
) -> dict:
    resp = {"status": status}
    if message_id:
        resp["message_id"] = message_id
    if data:
        resp["data"] = data
    return resp

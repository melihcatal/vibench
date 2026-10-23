import json
from typing import Any, Dict


class MessagePayload:
    """Normalize inbound/outbound message structures for all providers."""

    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.id: str = raw.get("id")
        self.timestamp: int = raw.get("timestamp", int(raw.get("ts", 0)))
        self.user_id = raw.get("user_id")
        self.data = raw.get("payload")
        self.metadata = raw.get("metadata", {})

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "payload": self.data,
            "metadata": self.metadata,
        }

    @staticmethod
    def normalize(raw: Dict[str, Any]) -> "MessagePayload":
        """Convert provider‑specific keys to a unified format."""
        normalized = {
            "id": raw.get("messageId") or raw.get("msg_id") or raw.get("id"),
            "timestamp": raw.get("eventTime")
            or raw.get("ts")
            or raw.get("time")
            or int(raw.get("timestamp", 0)),
            "user_id": raw.get("userId") or raw.get("user_id") or raw.get("uid"),
            "payload": raw.get("body") or raw.get("payload") or raw.get("data"),
            "metadata": raw.get("attributes") or raw.get("meta") or {},
        }
        # Ensure required fields are present, otherwise raise
        missing = [k for k in ("id", "timestamp", "payload") if not normalized[k]]
        if missing:
            raise ValueError(f"Missing required fields in message payload: {missing}")
        return MessagePayload(normalized)

    def __repr__(self):
        return f"MessagePayload(id={self.id}, ts={self.timestamp}, user={self.user_id})"

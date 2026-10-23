import json
from typing import Dict, Any


class Message:
    """Simple wrapper for a Pub/Sub message payload."""

    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        # Optionally normalize fields for internal use
        self.id = raw.get("id")
        self.action = raw.get("action")
        self.payload = raw.get("payload", {})
        self.timestamp = raw.get("timestamp")

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON‑serializable dict representation."""
        return self.raw


class Envelope:
    """Container for outbound messages with optional attributes."""

    def __init__(self, message: Message, headers: Dict[str, str] = None):
        self.message = message
        self.headers = headers or {}

    def as_dict(self) -> Dict[str, Any]:
        payload = self.message.to_dict()
        if self.headers:
            payload["headers"] = self.headers
        return payload

    def to_json(self) -> str:
        return json.dumps(self.as_dict())


# Utility to normalise incoming payloads (e.g., ensure required fields)
def normalize_event(raw: Dict[str, Any]) -> Message:
    # Example: enforce presence of id and action
    if not raw.get("id"):
        raise ValueError("Missing 'id' field in event")
    if not raw.get("action"):
        raise ValueError("Missing 'action' field in event")
    return Message(raw)


# Example usage (stand‑alone test)
if __name__ == "__main__":
    raw = {
        "id": "test-123",
        "action": "test_action",
        "payload": {"value": 42},
        "timestamp": "2024-01-01T00:00:00Z",
    }
    try:
        msg = normalize_event(raw)
        print("Normalized event:", msg.to_dict())
    except Exception as e:
        print("Normalization error:", e)

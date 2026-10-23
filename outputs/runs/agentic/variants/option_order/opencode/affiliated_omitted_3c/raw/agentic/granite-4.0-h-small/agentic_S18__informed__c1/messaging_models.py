import json
from typing import Dict, Any


class Message:
    """Wrapper for a normalized Pub/Sub message payload."""

    def __init__(self, raw_dict: Dict[str, Any]):
        self.raw = raw_dict
        # Normalize common fields to attributes
        self.id = raw_dict.get("id")
        self.payload = raw_dict.get("payload")
        self.metadata = raw_dict.get("metadata", {})

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""
        return {"id": self.id, "payload": self.payload, "metadata": self.metadata}


def normalize_event(event: Dict[str, Any]) -> Message:
    """Convert raw provider event to a standardized Message instance."""
    # Example normalization for Confluent Kafka (dict event)
    return Message(event)


def denormalize_response(message: Message, result: Any) -> Dict[str, Any]:
    """Create a standardized response dict from a processed message."""
    return {
        "message_id": message.id,
        "status": str(result),
        "processed_at": int(result) if isinstance(result, (int, float)) else "ok",
    }


if __name__ == "__main__":
    # Demo: normalize a sample dict and then denormalize
    raw = {"id": "demo", "payload": "demo payload", "metadata": {"source": "local"}}
    normalized = normalize_event(raw)
    print("Normalized:", normalized.to_dict())
    response = denormalize_response(normalized, 1)
    print("Response:", response)

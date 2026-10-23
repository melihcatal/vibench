from typing import Any, Dict


class MessagePayload:
    """Local model for normalized Pub/Sub message payload."""

    def __init__(self, data: Any, attributes: Dict[str, str] = None):
        self.data = data
        self.attributes = attributes or {}

    @classmethod
    def from_raw(cls, raw_msg):
        """Create a MessagePayload from a raw Pub/Sub message dict."""
        data = raw_msg.get("data")
        # Decode if data is bytes
        if isinstance(data, bytes):
            try:
                data = data.decode("utf-8")
            except UnicodeDecodeError:
                data = str(data)
        attributes = raw_msg.get("attributes", {})
        try:
            # Try JSON deserialization
            data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            pass
        return cls(data, attributes)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize payload back to dict for storage or audit."""
        return {"data": self.data, "attributes": self.attributes}


# Helper functions for payload normalization and validation
import json


def normalize_payload(raw_msg: Dict[str, Any]) -> MessagePayload:
    """Wrap MessagePayload.from_raw for convenience."""
    return MessagePayload.from_raw(raw_msg)


def is_safe_content(text: str) -> bool:
    """Placeholder safety check (replace with real moderation service if needed)."""
    unsafe_keywords = ["spam", "hate", "illegal"]
    return not any(word in text.lower() for word in unsafe_keywords)

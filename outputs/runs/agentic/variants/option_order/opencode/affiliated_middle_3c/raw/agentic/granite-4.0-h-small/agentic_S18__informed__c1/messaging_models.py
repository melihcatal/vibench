# messaging_models.py
# [HELPER]
# Local request, response, and normalization helpers for Pub/Sub messaging

import json
from typing import Dict, Any


def normalize_event(raw_event: Dict[str, Any]) -> Dict[str, Any]:
    """Convert raw webhook/HTTP payload into a canonical event dict."""
    # Ensure required fields exist, providing defaults where sensible
    event = {
        "id": raw_event.get("id") or str(uuid.uuid4()),
        "eventType": raw_event.get("type") or "generic",
        "payload": raw_event.get("payload") or {},
        "timestamp": raw_event.get("timestamp") or int(time.time()),
        "source": raw_event.get("source") or "unknown",
    }
    return event


def serialize_message(event: Dict[str, Any]) -> str:
    """Serialize a normalized event to a JSON string suitable for SNS/SQS."""
    # Perform JSON dump with sorted keys for reproducibility
    return json.dumps(event, sort_keys=True)


def deserialize_message(json_str: str) -> Dict[str, Any]:
    """Parse a JSON string back into a normalized event dictionary."""
    return json.loads(json_str)


def validate_event(event: Dict[str, Any]) -> bool:
    """Simple schema validation to guard against malformed messages."""
    required = {"id", "eventType", "payload", "timestamp", "source"}
    return required.issubset(event.keys())


if __name__ == "__main__":
    # Small demo of helpers (remove/comment out in real projects)
    import uuid, time

    raw = {"type": "demo", "payload": {"value": 123}}
    norm = normalize_event(raw)
    print("Normalized:", norm)
    s = serialize_message(norm)
    print("Serialized:", s)
    back = deserialize_message(s)
    print("Deserialized:", back)

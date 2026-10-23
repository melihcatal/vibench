import json
from typing import TypedDict, Optional, List


class EventPayload(TypedDict):
    """Example structure for an event that will be published via Pub/Sub."""
    event_id: str
    timestamp: int
    data: dict


class MessageRecord(TypedDict):
    """Record stored after successful processing (e.g., in a NoSQL store)."""
    message_id: str
    topic: str
    received_at: int
    payload: EventPayload
    processed_by: Optional[str] = None
    status: str = "processed"
    error: Optional[str] = None


# Helper to normalise a raw Pub/Sub payload (which is a dict) into our EventPayload

def normalize_event(raw: dict) -> EventPayload:
    """Cast incoming payload to the typed model, filling missing fields with defaults."""
    return {
        "event_id": raw.get("event_id", "unknown").strip() if raw.get("event_id") else "unknown",
        "timestamp": int(raw.get("timestamp", 0)),
        "data": raw.get("data", {}),
    }


def serialize_message(record: MessageRecord) -> str:
    """Convert a MessageRecord to a JSON string for persistence or logging."""
    return json.dumps(record)


# Example usage (not executed in this helper file)
# raw_msg = {...}  # from Pub/Sub
# event = normalize_event(raw_msg)
# record = MessageRecord(message_id=\"msg-123\", topic=\"my-topic\",
#                         received_at=int(time.time()), payload=event)
# persisted = serialize_message(record)

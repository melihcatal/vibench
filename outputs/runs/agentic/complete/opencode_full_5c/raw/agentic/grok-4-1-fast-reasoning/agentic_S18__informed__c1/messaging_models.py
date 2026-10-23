from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime
import json


@dataclass
class Event:
    id: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


def serialize_event(event: Event) -> bytes:
    return json.dumps(
        {
            "id": event.id,
            "event_type": event.event_type,
            "payload": event.payload,
            "timestamp": event.timestamp,
        }
    ).encode("utf-8")


def deserialize_event(data: bytes) -> Event:
    d = json.loads(data.decode("utf-8"))
    return Event(
        id=d["id"],
        event_type=d["event_type"],
        payload=d["payload"],
        timestamp=d["timestamp"],
    )

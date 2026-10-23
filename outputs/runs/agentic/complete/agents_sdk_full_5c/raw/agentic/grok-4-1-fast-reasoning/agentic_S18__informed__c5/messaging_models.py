import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict

@dataclass
class Event:
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['timestamp'] = d['timestamp'].isoformat()
        return d

@dataclass
class PubSubMessage:
    message_id: str
    data: str
    attributes: Dict[str, str] = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

def event_from_pubsub(msg: PubSubMessage) -> Event:
    event_data = json.loads(msg.data)
    event_data['timestamp'] = datetime.fromisoformat(event_data['timestamp'])
    return Event(**event_data)
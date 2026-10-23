import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class EventRequest:
    event_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps({"event_id": self.event_id, "payload": self.payload, "attributes": self.attributes}, separators=(",", ":"))


@dataclass
class EventResponse:
    message_id: str
    acknowledged: bool = True
    normalized_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class MessageRecord:
    message_id: str
    status: str
    body: str
    attributes: Dict[str, str] = field(default_factory=dict)
    processed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    return {str(key): str(value) for key, value in attributes.items()}


def parse_json_payload(data: bytes) -> Dict[str, Any]:
    return json.loads(data.decode("utf-8"))


def batch_payloads(events: Iterable[EventRequest]) -> List[bytes]:
    return [event.to_json().encode("utf-8") for event in events]

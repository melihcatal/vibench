import json
from typing import Dict, Any, Optional


class EventPayload:
    """Represents the structure of a generic event payload."""

    def __init__(
        self,
        data: Dict[str, Any],
        event_type: str,
        source: str,
        event_id: Optional[str] = None,
    ):
        self.data = data
        self.event_type = event_type
        self.source = source
        self.event_id = event_id

    def to_json_string(self) -> str:
        return json.dumps(
            {
                "data": self.data,
                "event_type": self.event_type,
                "source": self.source,
                "event_id": self.event_id,
            }
        )

    @classmethod
    def from_json_string(cls, json_string: str):
        data = json.loads(json_string)
        return cls(
            data=data.get("data", {}),
            event_type=data.get("event_type", ""),
            source=data.get("source", ""),
            event_id=data.get("event_id"),
        )


class PubSubMessage:
    """Represents a message with data and attributes for Pub/Sub."""

    def __init__(self, data: bytes, attributes: Optional[Dict[str, str]] = None):
        self.data = data
        self.attributes = attributes if attributes is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {"data": self.data, "attributes": self.attributes}

import json
from typing import Any, Dict

class EventMessage:
    """Local representation of a Pub/Sub event payload."""
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.event_id = data.get('event_id')
        self.payload = data.get('payload')
        self.metadata = data.get('metadata', {})

    @classmethod
class from_dict(cls, raw_json: str) -> 'EventMessage':
        """Deserialize a JSON string into an EventMessage."""
        data = json.loads(raw_json)
        return cls(data=data)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a dict suitable for API calls."""
        # Ensure required fields exist; add defaults if missing
        payload = self.data
        metadata = self.metadata
        return {
            'event_id': self.event_id or '',
            'payload': payload,
            'metadata': metadata,
        }

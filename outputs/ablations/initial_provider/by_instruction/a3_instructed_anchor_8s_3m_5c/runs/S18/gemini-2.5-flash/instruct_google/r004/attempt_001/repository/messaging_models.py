from typing import Any, Dict, List, Optional

# Placeholder for defining local request, response, and normalization helpers
class PubSubMessage:
    def __init__(self, data: bytes, message_id: str, attributes: Optional[Dict[str, str]] = None):
        self.data = data
        self.message_id = message_id
        self.attributes = attributes if attributes is not None else {}

    def to_json(self) -> Dict[str, Any]:
        return {
            "data": self.data.decode("utf-8"),
            "message_id": self.message_id,
            "attributes": self.attributes,
        }

class EventRequest:
    def __init__(self, event_type: str, payload: Dict[str, Any]):
        self.event_type = event_type
        self.payload = payload

class EventResponse:
    def __init__(self, success: bool, message_id: Optional[str] = None, error: Optional[str] = None):
        self.success = success
        self.message_id = message_id
        self.error = error

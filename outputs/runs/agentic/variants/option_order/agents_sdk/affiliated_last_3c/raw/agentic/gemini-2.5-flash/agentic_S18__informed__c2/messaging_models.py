import json
from typing import Dict, Any, Optional

class PubSubMessage:
    """A simple model to normalize Pub/Sub message data."""
    def __init__(self, data: bytes, attributes: Dict[str, str], message_id: Optional[str] = None):
        self._data = data
        self._attributes = attributes
        self._message_id = message_id

    @property
    def data(self) -> bytes:
        return self._data

    @property
    def attributes(self) -> Dict[str, str]:
        return self._attributes

    @property
    def message_id(self) -> Optional[str]:
        return self._message_id

    def get_json_data(self) -> Dict[str, Any]:
        """Decodes and parses message data as JSON."""
        try:
            return json.loads(self._data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Could not decode or parse JSON data: {e}")
            return {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "data": self.get_json_data(),
            "attributes": self.attributes,
        }

class ProcessedMessageResult:
    """Model for summarizing the result of message processing."""
    def __init__(self, message_id: str, status: str, details: Optional[str] = None):
        self.message_id = message_id
        self.status = status  # e.g., 'SUCCESS', 'FAILED', 'DEAD_LETTERED'
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "status": self.status,
            "details": self.details,
        }

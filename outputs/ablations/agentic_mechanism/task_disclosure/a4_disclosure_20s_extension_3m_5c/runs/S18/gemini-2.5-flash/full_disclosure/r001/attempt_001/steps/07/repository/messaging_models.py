import json
from typing import Dict, Any, Optional

class PubsubMessage:
    """Represents a message for Pub/Sub, either for publishing or consuming."""
    def __init__(self, data: bytes, attributes: Optional[Dict[str, str]] = None, message_id: Optional[str] = None):
        if not isinstance(data, bytes):
            raise TypeError("Message data must be bytes.")
        self.data: bytes = data
        self.attributes: Dict[str, str] = attributes if attributes is not None else {}
        self.message_id: Optional[str] = message_id

    def to_json_data(self) -> Dict[str, Any]:
        """Decodes message data from bytes to a JSON dictionary."""
        try:
            return json.loads(self.data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ValueError(f"Could not decode message data as JSON: {e}") from e

    @classmethod
    def from_json_data(cls, json_data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None) -> 'PubsubMessage':
        """Creates a PubsubMessage from a JSON dictionary."""
        data_bytes = json.dumps(json_data).encode('utf-8')
        return cls(data=data_bytes, attributes=attributes)

class PublishResponse:
    """Represents the response from a Pub/Sub publish operation."""
    def __init__(self, message_id: str):
        self.message_id: str = message_id

def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """Ensures attributes are a dictionary of string keys and string values."""
    if attributes is None:
        return {}
    normalized = {}
    for key, value in attributes.items():
        if not isinstance(key, str):
            key = str(key)
        if not isinstance(value, str):
            value = str(value)
        normalized[key] = value
    return normalized

import json
from typing import Dict, Any, Optional

class PubSubMessage:
    def __init__(self, data: Dict[str, Any], message_id: Optional[str] = None, attributes: Optional[Dict[str, str]] = None):
        self.data = data
        self.message_id = message_id
        self.attributes = attributes if attributes is not None else {}

    def to_json(self) -> str:
        return json.dumps(self.data)

    @classmethod
    def from_json(cls, json_str: str, message_id: Optional[str] = None, attributes: Optional[Dict[str, str]] = None):
        return cls(json.loads(json_str), message_id=message_id, attributes=attributes)

class AuditRecord:
    def __init__(self, message_id: str, timestamp: str, status: str, original_payload: Dict[str, Any], processed_payload: Dict[str, Any]):
        self.message_id = message_id
        self.timestamp = timestamp
        self.status = status
        self.original_payload = original_payload
        self.processed_payload = processed_payload

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "status": self.status,
            "original_payload": self.original_payload,
            "processed_payload": self.processed_payload,
        }

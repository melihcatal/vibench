from typing import Dict, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class EventMessage:
    id: str
    type: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, Any]] = None

    def to_json_string(self) -> str:
        return json.dumps({
            "id": self.id,
            "type": self.type,
            "data": self.data,
            "attributes": self.attributes
        })

    @classmethod
    def from_json_string(cls, json_string: str):
        data = json.loads(json_string)
        return cls(
            id=data["id"],
            type=data["type"],
            data=data["data"],
            attributes=data.get("attributes")
        )

@dataclass
class MessageProcessingResult:
    message_id: str
    status: str  # e.g., "success", "failed", "dead_lettered"
    details: Optional[str] = None
    processed_at: Optional[str] = None # ISO formatted datetime string


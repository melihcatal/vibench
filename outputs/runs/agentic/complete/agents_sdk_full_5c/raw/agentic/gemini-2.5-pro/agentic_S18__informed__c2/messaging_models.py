import json
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class SimpleMessage:
    """A simple dataclass for message payloads."""
    message_id: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Converts the dataclass instance to a dictionary."""
        return asdict(self)

    @classmethod
    def from_json(cls, json_str: str) -> "SimpleMessage":
        """Creates a SimpleMessage instance from a JSON string."""
        data = json.loads(json_str)
        return cls(message_id=data.get("message_id"), payload=data.get("payload"))

@dataclass
class ProcessingResult:
    """A dataclass to hold the result of message processing."""
    message_id: str
    status: str  # e.g., "SUCCESS", "FAILURE", "RETRY"
    details: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the dataclass instance to a dictionary."""
        return asdict(self)

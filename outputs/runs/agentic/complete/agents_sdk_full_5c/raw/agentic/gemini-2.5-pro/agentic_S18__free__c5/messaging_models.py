
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class EventPayload:
    """
    A structured model for a typical event message payload.
    """
    event_id: str
    user_id: str
    data: Dict[str, Any]

    def to_dict(self):
        """Converts the dataclass to a dictionary."""
        return asdict(self)

@dataclass
class ProcessingResult:
    """
    A model to hold the result of message processing.
    """
    original_event_id: str
    status: str  # e.g., "SUCCESS", "FAILURE", "RETRY"
    summary: str = None
    safety_check: Dict[str, float] = None
    translation: str = None
    audit_record_id: str = None
    error_message: str = None

    def to_dict(self):
        """Converts the dataclass to a dictionary."""
        return asdict(self)

def normalize_message_data(data: bytes) -> Dict:
    """
    Normalizes raw message data (bytes) into a Python dictionary.
    Placeholder for more complex logic like schema validation or transformation.
    """
    import json
    try:
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error normalizing message data: {e}")
        return {"error": "Invalid message format"}

from pydantic import BaseModel
from typing import Dict, Any, Optional


class Event(BaseModel):
    """Normalized event model for Pub/Sub messaging."""

    event_id: str
    event_type: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def dict(self) -> Dict[str, Any]:
        """Converts the event to a dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "data": self.data,
            "attributes": self.attributes or {},
        }

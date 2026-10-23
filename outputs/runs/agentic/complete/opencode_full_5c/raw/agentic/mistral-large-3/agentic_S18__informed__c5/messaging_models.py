from pydantic import BaseModel
from typing import Dict, Any, Optional


class Event(BaseModel):
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "attributes": self.attributes or {},
        }

from pydantic import BaseModel
from typing import Optional, Dict, Any

class EventMessage(BaseModel):
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

class DeadLetterMessage(BaseModel):
    original_message: Dict[str, Any]
    error: str
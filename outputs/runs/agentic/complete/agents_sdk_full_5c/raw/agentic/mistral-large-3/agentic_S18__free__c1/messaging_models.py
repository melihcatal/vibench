from pydantic import BaseModel
from typing import Optional, Dict, Any

class EventRequest(BaseModel):
    event_id: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

class EventResponse(BaseModel):
    event_id: str
    payload: Dict[str, Any]
    message_id: str
    attributes: Optional[Dict[str, str]] = None

class DeadLetterRequest(BaseModel):
    original_message: Dict[str, Any]
    error: str

class BatchEventRequest(BaseModel):
    event_id: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
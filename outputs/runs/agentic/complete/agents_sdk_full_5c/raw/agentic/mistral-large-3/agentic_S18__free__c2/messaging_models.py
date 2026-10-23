from pydantic import BaseModel
from typing import Dict, Any, Optional

class EventRequest(BaseModel):
    payload: Dict[str, Any]
    attributes: Dict[str, str] = {}

class EventResponse(BaseModel):
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    ack_id: str

class DeadLetterRequest(BaseModel):
    payload: Dict[str, Any]
    error: str
    original_message_id: str

class BatchEventRequest(BaseModel):
    payload: Dict[str, Any]
    message_id: str
    attributes: Dict[str, str] = {}

class ProcessedMessage(BaseModel):
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    processed_at: str
    is_safe: Optional[bool] = None
    summary: Optional[str] = None
    translated_payload: Optional[Dict[str, Any]] = None
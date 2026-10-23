from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class PubSubEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: str
    payload: Dict[str, Any]

class PubSubMessage(BaseModel):
    message_id: str
    body: str
    receipt_handle: Optional[str] = None
    attributes: Dict[str, str] = {}

class AuditRecord(BaseModel):
    message_id: str
    processed_at: str
    summary: Optional[str] = None
    safety_score: Optional[float] = None
    translated_payload: Optional[str] = None

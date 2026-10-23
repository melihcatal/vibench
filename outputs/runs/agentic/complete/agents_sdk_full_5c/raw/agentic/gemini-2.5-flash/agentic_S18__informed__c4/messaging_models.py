from pydantic import BaseModel
from typing import Optional, Dict, Any

class PubSubMessage(BaseModel):
    data: str
    attributes: Optional[Dict[str, str]] = None

class AuditRecord(BaseModel):
    message_id: str
    timestamp: str
    status: str
    summary: Optional[str] = None
    safety_check: Optional[Dict[str, Any]] = None
    translated_payload: Optional[str] = None

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uuid

class BaseMessage(BaseModel):
    """A generic message model for pub/sub payloads."""
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    attributes: Optional[Dict[str, Any]] = None

class AuditEvent(BaseModel):
    """A model for storing processed message records."""
    event_id: str
    original_message_id: str
    status: str
    summary: Optional[str] = None
    safety_scores: Optional[Dict[str, float]] = None
    translation: Optional[str] = None
    error_message: Optional[str] = None
    timestamp: str

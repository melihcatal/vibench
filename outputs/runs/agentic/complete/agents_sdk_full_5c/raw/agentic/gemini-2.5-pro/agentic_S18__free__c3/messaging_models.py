from typing import Optional, Dict
from pydantic import BaseModel, Field

class EventPayload(BaseModel):
    """A generic event payload model."""
    event_id: str = Field(..., description="Unique identifier for the event.")
    user_id: Optional[str] = None
    data: Dict

class AuditRecord(BaseModel):
    """A model for storing processed message details for auditing."""
    message_id: str
    subscription_path: str
    publish_time: str
    data: dict
    processing_outcome: str
    summary: Optional[str] = None
    is_safe: Optional[bool] = None
    translation: Optional[str] = None
    error_message: Optional[str] = None

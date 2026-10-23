
from pydantic import BaseModel, Field
from typing import Dict, Any

class EventPayload(BaseModel):
    """
    Defines the structure for a message payload.
    """
    request_id: str = Field(..., description="Unique identifier for the request.")
    user_id: str = Field(..., description="Identifier for the user associated with the event.")
    data: Dict[str, Any] = Field(..., description="The actual event data.")

class ProcessedMessage(BaseModel):
    """
    Represents a message after it has been processed, including results.
    """
    original_payload: EventPayload
    is_safe: bool
    summary: str | None = None
    translation: str | None = None
    status: str = "processed"
    error: str | None = None

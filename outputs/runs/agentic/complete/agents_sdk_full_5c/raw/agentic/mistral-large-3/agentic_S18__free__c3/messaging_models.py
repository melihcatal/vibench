from pydantic import BaseModel, Field
from typing import Dict, Optional

class EventMessage(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    payload: dict = Field(..., description="Event payload data")
    attributes: Dict[str, str] = Field(default_factory=dict, description="Message attributes")

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data.update(self.payload)
        return data

class BatchEventMessage(EventMessage):
    message_id: str = Field(..., description="Unique message identifier for batch publishing")

class DeadLetterMessage(BaseModel):
    original_message: dict = Field(..., description="Original failed message")
    error: str = Field(..., description="Error description")
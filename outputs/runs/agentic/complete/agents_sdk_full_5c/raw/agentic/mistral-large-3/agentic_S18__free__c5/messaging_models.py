from pydantic import BaseModel, Field
from typing import Dict, Optional

class EventMessage(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    payload: Dict = Field(..., description="Event payload data")
    attributes: Dict[str, str] = Field(default_factory=dict, description="Message attributes")
    
    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data["event_id"] = self.event_id
        data["payload"] = self.payload
        return data
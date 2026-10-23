from pydantic import BaseModel, Field
from typing import Dict, Optional

class EventMessage(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    payload: dict = Field(..., description="Event payload data")
    attributes: Dict[str, str] = Field(default_factory=dict, description="Message attributes")
    
    def dict(self, **kwargs):
        base_dict = super().dict(**kwargs)
        base_dict.update(self.payload)
        return base_dict
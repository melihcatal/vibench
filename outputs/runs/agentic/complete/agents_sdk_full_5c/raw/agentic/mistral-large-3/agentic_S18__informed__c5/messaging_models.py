from pydantic import BaseModel, Field
from typing import Dict, Optional

class Event(BaseModel):
    message_id: Optional[str] = None
    payload: Dict = Field(default_factory=dict)
    attributes: Dict[str, str] = Field(default_factory=dict)
    
    def model_dump_json(self) -> str:
        return self.model_dump_json(exclude={"message_id"})
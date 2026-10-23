
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import datetime

class StructuredLog(BaseModel):
    """

    A Pydantic model for a structured log entry.
    """
    message: str
    severity: str = 'INFO'
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    user_id: Optional[str] = None
    service_context: str = 'default-service'
    request_id: Optional[str] = None
    http_request: Optional[Dict[str, Any]] = None
    custom_dimensions: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat() + "Z"
        }
        
    def to_dict(self):
        return self.model_dump(exclude_none=True)

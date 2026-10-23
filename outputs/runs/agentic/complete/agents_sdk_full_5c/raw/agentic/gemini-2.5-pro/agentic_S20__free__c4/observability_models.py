from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import datetime

class StructuredLog(BaseModel):
    """
    A Pydantic model for a structured log entry.
    """
    message: str
    user_id: Optional[str] = None
    service_context: str = Field(default="python-app")
    request_method: Optional[str] = None
    request_url: Optional[str] = None
    response_status_code: Optional[int] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    extra_data: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the model to a dictionary for logging."""
        return self.model_dump(exclude_none=True)

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import datetime
import uuid

class StructuredLog(BaseModel):
    message: str
    severity: str = "INFO"
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now(datetime.timezone.utc))
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    service_context: Dict[str, Any] = {"service": "my-python-app"}
    http_request: Optional[Dict[str, Any]] = None
    custom_dimensions: Dict[str, Any] = Field(default_factory=dict)

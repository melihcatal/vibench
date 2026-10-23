from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import datetime


class StructuredLog(BaseModel):
    message: str
    severity: str = Field(default="INFO")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    context: Optional[Dict[str, Any]] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None

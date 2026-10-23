from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class LogEvent(BaseModel):
    message: str
    severity: Optional[str] = "INFO"
    service: str = "myapp"
    env: str = "prod"
    hostname: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

    def datadog_payload(self) -> Dict[str, Any]:
        payload = self.dict(exclude_none=True)
        payload["ddsource"] = "python-integration"
        payload["ddtags"] = f"env:{self.env},service:{self.service}"
        if self.timestamp:
            payload["date"] = int(self.timestamp.timestamp() * 1000)
        return payload

class LogsQueryParams(BaseModel):
    query: str
    time: Dict[str, int]
    page: Dict[str, Any] = Field(default_factory=lambda: {"limit": 100})

    class Config:
        populate_by_field_name = True
        allow_population_by_field_name = True

class QueryResponse(BaseModel):
    data: List[Dict[str, Any]]
    meta: Optional[Dict[str, Any]] = None
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class LogEvent(BaseModel):
    message: str
    level: str = "info"
    service: str = "myapp"
    env: str = "prod"
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None


class QueryParams(BaseModel):
    query: str
    from_timestamp: int
    to_timestamp: int
    limit: int = 10


class LogEntry(BaseModel):
    id: str
    attributes: Dict[str, Any]


class QueryResponse(BaseModel):
    logs: List[LogEntry]

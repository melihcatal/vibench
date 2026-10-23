from datetime import datetime
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class LogEvent(BaseModel):
    timestamp_ms: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    message: Dict[str, Any]
    log_group: str
    log_stream: str


class CorrelatedLogEvent(BaseModel):
    timestamp_ms: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    correlation_id: str
    message: Dict[str, Any]
    log_group: str
    log_stream: str


class QueryLogsRequest(BaseModel):
    log_group_name: str
    start_time_ms: int
    end_time_ms: int
    filter_pattern: Optional[str] = None
    limit: int = 100


class QueryLogsResponse(BaseModel):
    events: list[Dict[str, Any]]
    next_token: Optional[str] = None

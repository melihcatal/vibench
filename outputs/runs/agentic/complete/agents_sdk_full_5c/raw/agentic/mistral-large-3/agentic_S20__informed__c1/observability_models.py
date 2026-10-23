from datetime import datetime
from typing import Dict, Optional, List
from pydantic import BaseModel


class LogEntry(BaseModel):
    severity: str
    message: str
    timestamp: datetime
    labels: Dict[str, str] = {}
    custom_fields: Dict[str, str] = {}


class CorrelatedLogEntry(LogEntry):
    correlation_id: str


class ErrorLogFilter(BaseModel):
    min_severity: str
    start_time: datetime
    end_time: datetime
    max_results: int = 100


class RecentLogFilter(BaseModel):
    log_name: str
    start_time: datetime
    end_time: datetime
    field_filters: Dict[str, str] = {}
    max_results: int = 100
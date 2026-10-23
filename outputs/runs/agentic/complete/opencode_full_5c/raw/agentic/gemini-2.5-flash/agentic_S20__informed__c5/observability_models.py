from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class StructuredLogEntry(BaseModel):
    message: str
    severity: str = "INFO"
    timestamp: datetime = datetime.utcnow()
    json_payload: Dict[str, Any] = {}
    resource_type: str = "global"
    resource_labels: Dict[str, str] = {}


class CorrelatedLogEntry(BaseModel):
    message: str
    correlation_id: str
    severity: str = "INFO"
    timestamp: datetime = datetime.utcnow()
    json_payload: Dict[str, Any] = {}
    resource_type: str = "global"
    resource_labels: Dict[str, str] = {}


class LogQueryParameters(BaseModel):
    project_id: str
    filter_string: str
    order_by: str = "timestamp desc"
    limit: int = 100
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

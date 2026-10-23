from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class LogPayload(BaseModel):
    severity: str = Field('INFO', description='Log severity level.')
    message: str = Field(..., description='Primary log message.')
    details: Dict[str, Any] = Field({}, description='Optional structured details.')

class LogRequest(BaseModel):
    resource: str = Field(..., description='Monitored resource type (e.g., "global").')
    correlation_id: str = Field(..., description='Shared request/trace ID.')
    log: LogPayload = Field(..., description='The log payload model.')

class ErrorLogFilter(BaseModel):
    start_time: datetime
    end_time: datetime
    severity: str = Field('ERROR', description='Severity filter, default is ERROR.')

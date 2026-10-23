from typing import TypedDict, Dict, Any, Optional
from datetime import datetime, timedelta

class StructuredLog(TypedDict):
    message: str
    severity: str
    correlation_id: Optional[str]
    service: str
    metadata: Optional[Dict[str, Any]]

def get_error_log_filter(hours_back: int = 24) -> str:
    end_time = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    start_time = (datetime.utcnow() - timedelta(hours=hours_back)).isoformat(timespec='milliseconds') + 'Z'
    return f'severity &gt;= "ERROR" timestamp &gt;= "{start_time}" timestamp &lt;= "{end_time}"'

def get_service_log_filter(service_name: str, hours_back: int = 1) -> str:
    end_time = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    start_time = (datetime.utcnow() - timedelta(hours=hours_back)).isoformat(timespec='milliseconds') + 'Z'
    return f'jsonPayload.service = "{service_name}" timestamp &gt;= "{start_time}" timestamp &lt;= "{end_time}"'
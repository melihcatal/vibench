from observability_client import get_logging_client
from observability_models import LogQueryResult
from datetime import datetime, timedelta
from typing import List, Dict, Any

def fetch_recent_logs_by_fields(log_name: str, field_filters: Dict[str, Any], time_range_minutes: int = 60) -> List[LogQueryResult]:
    client = get_logging_client()
    
    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)
    
    filter_string = (
        f'logName="projects/{client.project}/logs/{log_name}" '
        f'timestamp >= "{start_time.isoformat(timespec="seconds")}Z"'
    )
    
    for field, value in field_filters.items():
        filter_string += f' jsonPayload.{field}="{value}"'
        
    results: List[LogQueryResult] = []
    for entry in client.list_entries(filter_=filter_string, order_by="timestamp desc"):
        timestamp = entry.timestamp
        severity = entry.severity
        
        message = ""
        payload = {}
        if entry.json_payload:
            payload = entry.json_payload
            message = payload.get("message", str(payload))
        elif entry.text_payload:
            message = entry.text_payload
            payload = {"textPayload": entry.text_payload}
        elif entry.proto_payload:
            message = str(entry.proto_payload)
            payload = {"protoPayload": str(entry.proto_payload)}
        
        results.append(LogQueryResult(
            timestamp=timestamp,
            severity=severity,
            message=message,
            full_payload=payload
        ))
    return results
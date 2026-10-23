import os
from datetime import datetime
from typing import List
from observability_client import get_log_client
from observability_models import CorrelatedLogEvent

def write_correlated_logs(correlation_id: str, events: List[dict]) -> List[str]:
    client = get_log_client()
    log_entries = []
    for event in events:
        log_event = CorrelatedLogEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            severity=event.get("severity", "INFO"),
            message=event.get("message", ""),
            correlation_id=correlation_id,
            attributes=event
        )
        log_entries.append({
            "time": log_event.timestamp,
            "severity": log_event.severity,
            "message": log_event.message,
            "attributes": {
                **log_event.attributes,
                "correlation_id": log_event.correlation_id
            }
        })

    response = client.logs.ingest(
        body={
            "logs": log_entries,
            "resource": {
                "type": "global",
                "labels": {
                    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT", "default-project")
                }
            }
        }
    )
    return [entry.get("logId", "") for entry in response.get("logs", [])]
from observability_client import ObservabilityClient
from observability_models import LogEntry
from datetime import datetime, timezone
import uuid
import os

def write_correlated_logs(resource_type: str, resource_id: str, correlation_id: str, messages: list[dict], project_id: str = None):
    client = ObservabilityClient(project_id=project_id)
    
    log_entries = []
    for msg in messages:
        log_entry = LogEntry(
            severity=msg.get("severity", "INFO"),
            message=msg.get("message", ""),
            resource_type=resource_type,
            resource_id=resource_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            labels={
                "correlation_id": correlation_id,
                **msg.get("labels", {})
            },
            json_payload=msg.get("json_payload")
        )
        client.write_log_entry(log_entry)
        log_entries.append(log_entry)
    
    return {"submitted_count": len(log_entries), "correlation_id": correlation_id}

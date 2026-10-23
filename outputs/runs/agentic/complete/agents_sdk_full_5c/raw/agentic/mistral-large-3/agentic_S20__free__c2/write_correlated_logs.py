import json
import os
from datetime import datetime
from observability_client import get_logging_client

def write_correlated_logs(correlation_id: str, events: list[dict]):
    client = get_logging_client()
    
    log_entries = []
    for event in events:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": event.get("severity", "INFO"),
            "message": event.get("message", ""),
            "service": event.get("service", "unknown"),
            "correlation_id": correlation_id,
            "details": event.get("details", {})
        }
        log_entries.append({
            "message": json.dumps(log_entry),
            "ddsource": "python-integration",
            "ddtags": f"service:{log_entry['service']},correlation_id:{correlation_id}",
            "hostname": os.getenv("HOSTNAME", "unknown")
        })
    
    # Bulk ingestion via Datadog API
    response = client.submit_logs(body=log_entries)
    return response
import json
import os
from datetime import datetime
from observability_client import get_logging_client

def write_structured_log(event_data: dict):
    client = get_logging_client()
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "severity": event_data.get("severity", "INFO"),
        "message": event_data.get("message", ""),
        "service": event_data.get("service", "unknown"),
        "details": event_data.get("details", {})
    }
    
    # Datadog API-specific structured log ingestion
    response = client.submit_log(
        body={
            "message": json.dumps(log_entry),
            "ddsource": "python-integration",
            "ddtags": f"service:{log_entry['service']}",
            "hostname": os.getenv("HOSTNAME", "unknown")
        }
    )
    return response
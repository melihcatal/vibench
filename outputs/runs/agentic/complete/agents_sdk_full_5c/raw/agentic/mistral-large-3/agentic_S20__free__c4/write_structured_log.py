import json
import os
from datetime import datetime
from observability_client import get_log_client
from observability_models import StructuredLogEvent

def write_structured_log(event_data: dict, severity: str = "INFO") -> str:
    client = get_log_client()
    event = StructuredLogEvent(
        timestamp=datetime.utcnow().isoformat() + "Z",
        severity=severity,
        message=event_data.get("message", ""),
        attributes=event_data
    )
    response = client.logs.ingest(
        body={
            "logs": [{
                "time": event.timestamp,
                "severity": event.severity,
                "message": event.message,
                "attributes": event.attributes
            }],
            "resource": {
                "type": "global",
                "labels": {
                    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT", "default-project")
                }
            }
        }
    )
    return response.get("logId", "")
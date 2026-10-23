import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent

def write_structured_log(event_data: dict, severity: str = "INFO") -> str:
    client = get_logging_client()
    event = StructuredLogEvent(
        timestamp=datetime.utcnow().isoformat() + "Z",
        severity=severity,
        message=event_data.get("message", ""),
        attributes=event_data
    )
    response = client.logs.log_event(
        project_name=os.getenv("DATADOG_PROJECT", "default"),
        body={
            "message": json.dumps(event.dict()),
            "ddsource": "python-integration",
            "ddtags": f"severity:{severity}",
            "hostname": os.getenv("HOSTNAME", "unknown")
        }
    )
    return response.get("id")
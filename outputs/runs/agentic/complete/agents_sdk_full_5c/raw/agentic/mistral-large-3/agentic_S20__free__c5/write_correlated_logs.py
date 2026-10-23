import os
from datetime import datetime
from typing import List
from observability_client import get_logging_client
from observability_models import CorrelatedLogEvent

def write_correlated_logs(events: List[dict], correlation_id: str) -> List[str]:
    client = get_logging_client()
    log_ids = []
    for event_data in events:
        event = CorrelatedLogEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            severity=event_data.get("severity", "INFO"),
            message=event_data.get("message", ""),
            correlation_id=correlation_id,
            attributes=event_data
        )
        response = client.logs.log_event(
            project_name=os.getenv("DATADOG_PROJECT", "default"),
            body={
                "message": event.message,
                "ddsource": "python-integration",
                "ddtags": f"severity:{event.severity},correlation_id:{correlation_id}",
                "hostname": os.getenv("HOSTNAME", "unknown"),
                "attributes": event.attributes
            }
        )
        log_ids.append(response.get("id"))
    return log_ids
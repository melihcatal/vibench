from datetime import datetime, timezone
from observability_client import get_logging_client
from google.cloud.logging_v2.resource import Resource
import os

def write_correlated_logs(log_name: str, correlation_id: str, events: list[dict]):
    client = get_logging_client()
    logger = client.logger(log_name)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    for event in events:
        payload = {
            "correlation_id": correlation_id,
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        logger.log_struct(
            payload,
            severity=event.get("severity", "INFO"),
            timestamp=datetime.now(timezone.utc),
            resource=Resource(type="global", labels={"project_id": project_id}),
        )
    return {"submitted": True, "correlation_id": correlation_id, "event_count": len(events)}

from datetime import datetime, timezone
import time

from observability_client import ObservabilityClient
from observability_models import LogEntry
from google.cloud.logging_v2.resource import Resource

def write_correlated_logs(correlation_id, events, config=None):
    config = config or {}
    client = ObservabilityClient(project_id=config["project_id"])
    logging_client = client.get_logging_client()
    logger = logging_client.logger(config["log_name"])

    for event in events:
        payload = {"correlation_id": correlation_id, "event": event}
        timestamp_ms = event.get("timestamp_ms", time.time() * 1000)
        logger.log_struct(
            payload,
            timestamp=datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc),
            resource=Resource(type="global", labels={"project_id": config["project_id"]}),
        )
    return {"submitted": True, "correlation_id": correlation_id}

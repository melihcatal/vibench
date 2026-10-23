from datetime import datetime, timezone
import time
from google.cloud.logging_v2.resource import Resource

from observability_client import get_logging_client
from observability_models import CorrelatedLogEvent


def write_correlated_logs(event: CorrelatedLogEvent):
    client = get_logging_client(event.project_id)
    logger = client.logger(event.log_name)
    timestamp_ms = event.timestamp_ms or (time.time() * 1000)

    log_entry = {
        "event": event.event,
        "correlation_id": event.correlation_id,
    }

    logger.log_struct(
        log_entry,
        timestamp=datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc),
        resource=Resource(type="global", labels={"project_id": event.project_id}),
    )
    return {"submitted": True, "correlation_id": event.correlation_id}

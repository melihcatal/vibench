from datetime import datetime, timezone
import time
import uuid

from google.cloud import logging_v2
from google.cloud.logging_v2.resource import Resource
from observability_client import ObservabilityClient
from observability_models import LogEntry

def write_correlated_logs(log_name: str, messages: list[str], correlation_id: str = None, project_id: str = None):
    client = ObservabilityClient(project_id=project_id)
    logger = client.get_logger(log_name)
    correlation_id = correlation_id or str(uuid.uuid4())

    for message in messages:
        log_entry = LogEntry(
            message=message,
            severity="INFO",
            trace_id=correlation_id,
            labels={"correlation_id": correlation_id},
            metadata={"app_name": "my-service"}
        )
        logger.log_struct(
            log_entry.model_dump(by_alias=True, exclude_none=True),
            timestamp=datetime.fromtimestamp(log_entry.timestamp.timestamp(), tz=timezone.utc),
            resource=Resource(type="global", labels={"project_id": client.project_id}),
        )
    return {"submitted_count": len(messages), "correlation_id": correlation_id}

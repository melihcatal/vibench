from datetime import datetime, timezone
import time
import uuid

from google.cloud import logging_v2
from google.cloud.logging_v2.resource import Resource

from observability_client import load_config
from observability_models import build_event


def write_correlated_logs(payload, config=None):
    config = load_config(config)
    client = logging_v2.Client(project=config["project_id"])
    logger = client.logger(config["log_name"])
    correlation_id = payload.get("correlation_id") or str(uuid.uuid4())
    base_timestamp_ms = payload.get("timestamp_ms", time.time() * 1000)
    entries = []
    for index, event in enumerate(payload.get("events", [])):
        entries.append(
            logger.log_struct(
                build_event(
                    event.get("message", "log event"),
                    event.get("severity", "INFO"),
                    correlation_id=correlation_id,
                    sequence=index,
                    service=config["service_name"],
                ),
                timestamp=datetime.fromtimestamp((base_timestamp_ms + index) / 1000, tz=timezone.utc),
                resource=Resource(type="global", labels={"project_id": config["project_id"]}),
            )
        )
    return {"submitted": True, "correlation_id": correlation_id, "count": len(entries)}

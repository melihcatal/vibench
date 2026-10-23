import uuid

from google.cloud import logging_v2
from google.cloud.logging_v2.resource import Resource

from observability_client import make_client
from observability_models import LogEvent


def write_correlated_logs(payload, config=None):
    cfg, client = make_client(config)
    logger = client.logger(cfg.log_name)
    correlation_id = payload.get("correlation_id") or str(uuid.uuid4())
    events = payload.get("events") or []
    submitted = []
    for item in events:
        event = LogEvent(
            message=item["message"],
            severity=item.get("severity", "INFO"),
            correlation_id=correlation_id,
            service=cfg.service_name,
            timestamp_ms=item.get("timestamp_ms", 0),
        ).as_struct()
        logger.log_struct(
            event,
            resource=Resource(type="global", labels={"project_id": cfg.project_id}),
        )
        submitted.append(event)
    return {"submitted": True, "correlation_id": correlation_id, "events": submitted}

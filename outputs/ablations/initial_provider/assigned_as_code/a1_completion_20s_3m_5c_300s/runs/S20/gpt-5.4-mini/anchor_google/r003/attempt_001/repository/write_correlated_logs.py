from datetime import datetime, timezone

from google.cloud import logging_v2
from google.cloud.logging_v2.resource import Resource

from observability_client import get_logging_client
from observability_models import build_log_event


def write_correlated_logs(payload, config=None):
    client, cfg = get_logging_client(config)
    logger = client.logger(cfg["log_name"])
    request_id = payload["request_id"]
    events = payload["events"]
    for event in events:
        timestamp = event.get("timestamp") or datetime.now(timezone.utc)
        logger.log_struct(
            build_log_event(
                event["message"],
                event.get("severity", "INFO"),
                request_id=request_id,
                **{k: v for k, v in event.items() if k not in {"message", "severity", "timestamp"}},
            ),
            timestamp=timestamp,
            resource=Resource(type="global", labels={"project_id": cfg["project_id"]}),
        )
    return {"submitted": True, "request_id": request_id, "count": len(events)}

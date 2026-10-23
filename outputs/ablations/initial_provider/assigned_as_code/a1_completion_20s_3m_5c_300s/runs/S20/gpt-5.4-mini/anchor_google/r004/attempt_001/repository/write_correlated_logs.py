from google.cloud import logging_v2

from observability_client import build_client, isoformat
from observability_models import normalize_event


def write_correlated_logs(payload, config=None):
    client, config = build_client(config)
    logger = client.logger(config["log_name"])
    correlation_id = payload["correlation_id"]
    events = [
        normalize_event(event, {"correlation_id": correlation_id}) for event in payload["events"]
    ]
    logger.batch().log_struct(events)
    return {"submitted": True, "correlation_id": correlation_id, "event_count": len(events)}

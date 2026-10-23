from google.cloud import logging_v2
from google.cloud.logging_v2.resource import Resource

from observability_client import build_client
from observability_models import normalize_payload


def write_correlated_logs(payload, config=None):
    client, config = build_client(config)
    logger = client.logger(config["log_name"])
    correlation_id = payload["correlation_id"]
    entries = []
    for item in payload["events"]:
        event = normalize_payload(item)
        event["correlation_id"] = correlation_id
        entries.append((event, item.get("severity", "INFO")))
    for event, severity in entries:
        logger.log_struct(event, severity=severity, resource=Resource(type="global", labels={"project_id": config["project_id"]}))
    return {"submitted": True, "correlation_id": correlation_id}

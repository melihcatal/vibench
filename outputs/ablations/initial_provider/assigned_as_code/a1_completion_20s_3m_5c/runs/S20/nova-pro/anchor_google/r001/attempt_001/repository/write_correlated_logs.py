from google.cloud import logging_v2
from google.cloud.logging_v2.resource import Resource

def write_correlated_logs(payload, config=None):
    config = config or {}
    client = logging_v2.Client(project=config["project_id"])
    logger = client.logger(config["log_name"])
    timestamp_ms = payload.get("timestamp_ms", time.time() * 1000)
    logger.log_struct(
        payload["event"],
        timestamp=datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc),
        resource=Resource(type="global", labels={"project_id": config["project_id"]}),
        correlation=payload["correlation_id"],
    )
    return {"submitted": True}
from datetime import datetime, timezone

from google.cloud import logging_v2

from observability_client import build_client
from observability_models import LogQueryRequest, to_rfc3339


def query_error_logs(payload, config=None):
    client, config = build_client(config)
    request = LogQueryRequest(
        severity=payload.get("severity", "ERROR"),
        start_time=to_rfc3339(payload.get("start_time")),
        end_time=to_rfc3339(payload.get("end_time")),
    )
    logger = client.logger(config["log_name"])
    _ = logger
    query = [f'severity>={request.severity}']
    if request.start_time:
        query.append(f'timestamp>="{request.start_time}"')
    if request.end_time:
        query.append(f'timestamp<="{request.end_time}"')
    return {"filter": " AND ".join(query), "submitted": True}

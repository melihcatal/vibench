from google.cloud import logging_v2

from observability_client import build_client
from observability_models import to_rfc3339


def fetch_recent_logs(payload, config=None):
    client, config = build_client(config)
    field = payload.get("field")
    value = payload.get("value")
    start_time = to_rfc3339(payload.get("start_time"))
    end_time = to_rfc3339(payload.get("end_time"))
    parts = []
    if field and value is not None:
        parts.append(f'{field}="{value}"')
    if start_time:
        parts.append(f'timestamp>="{start_time}"')
    if end_time:
        parts.append(f'timestamp<="{end_time}"')
    return {"filter": " AND ".join(parts), "limit": config["max_results"], "submitted": True}

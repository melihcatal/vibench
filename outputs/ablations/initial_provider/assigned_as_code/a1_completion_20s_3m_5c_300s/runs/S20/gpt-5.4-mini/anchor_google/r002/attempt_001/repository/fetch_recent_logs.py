from datetime import datetime, timezone

from google.cloud import logging_v2

from observability_client import load_config


def fetch_recent_logs(payload, config=None):
    config = load_config(config)
    client = logging_v2.Client(project=config["project_id"])
    field_name = payload.get("field_name")
    field_value = payload.get("field_value")
    start_ms = payload.get("start_ms")
    end_ms = payload.get("end_ms")
    filters = [f'logName="projects/{config["project_id"]}/logs/{config["log_name"]}"']
    if field_name and field_value is not None:
        filters.append(f'{field_name}="{field_value}"')
    if start_ms is not None:
        filters.append(f'timestamp>="{datetime.fromtimestamp(start_ms / 1000, tz=timezone.utc).isoformat()}"')
    if end_ms is not None:
        filters.append(f'timestamp<="{datetime.fromtimestamp(end_ms / 1000, tz=timezone.utc).isoformat()}"')
    entries = client.list_entries(filter_=" AND ".join(filters), order_by=logging_v2.DESCENDING, page_size=payload.get("limit", 50))
    return {"entries": [entry.to_api_repr() for entry in entries]}

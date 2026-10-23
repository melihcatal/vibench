from google.cloud import logging_v2

from observability_client import build_client, isoformat


def fetch_recent_logs(payload, config=None):
    client, config = build_client(config)
    filters = []
    for field, value in (payload.get("field_values") or {}).items():
        filters.append(f'{field}="{value}"')
    if payload.get("start_time"):
        filters.append(f'timestamp>="{isoformat(payload["start_time"])}"')
    if payload.get("end_time"):
        filters.append(f'timestamp<="{isoformat(payload["end_time"])}"')
    if payload.get("log_name"):
        filters.append(f'logName="projects/{config["project_id"]}/logs/{payload["log_name"]}"')
    query = " AND ".join(filters) if filters else None
    entries = list(client.list_entries(filter_=query, page_size=payload.get("limit", 100)))
    return {"query": query, "entries": [entry.to_api_repr() for entry in entries]}

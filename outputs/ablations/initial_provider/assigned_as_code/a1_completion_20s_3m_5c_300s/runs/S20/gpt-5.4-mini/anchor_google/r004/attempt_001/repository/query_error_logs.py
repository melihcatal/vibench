from google.cloud import logging_v2

from observability_client import build_client, isoformat, to_datetime


def query_error_logs(payload, config=None):
    client, config = build_client(config)
    start_time = isoformat(payload.get("start_time"))
    end_time = isoformat(payload.get("end_time"))
    severity = payload.get("severity", "ERROR")
    filter_parts = [f'severity>={severity}']
    if payload.get("log_name"):
        filter_parts.append(f'logName="projects/{config["project_id"]}/logs/{payload["log_name"]}"')
    if start_time:
        filter_parts.append(f'timestamp>="{start_time}"')
    if end_time:
        filter_parts.append(f'timestamp<="{end_time}"')
    query = " AND ".join(filter_parts)
    entries = list(client.list_entries(filter_=query, page_size=payload.get("limit", 50)))
    return {"query": query, "entries": [entry.to_api_repr() for entry in entries]}

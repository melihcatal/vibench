from google.cloud import logging_v2

from observability_client import load_config


def incident_summary(payload, config=None):
    config = load_config(config)
    client = logging_v2.Client(project=config["project_id"])
    correlation_id = payload.get("correlation_id")
    filter_parts = [f'logName="projects/{config["project_id"]}/logs/{config["log_name"]}"', 'severity>=ERROR']
    if correlation_id:
        filter_parts.append(f'jsonPayload.correlation_id="{correlation_id}"')
    entries = list(client.list_entries(filter_=" AND ".join(filter_parts), page_size=payload.get("limit", 20)))
    return {"error_count": len(entries), "correlation_id": correlation_id, "sample_entries": [entry.to_api_repr() for entry in entries[:3]]}

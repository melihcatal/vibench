from datetime import datetime, timedelta, timezone

from google.cloud import logging_v2

from observability_client import make_client


def fetch_recent_logs(payload, config=None):
    cfg, client = make_client(config)
    minutes = int(payload.get("minutes", 30))
    field = payload.get("field", "severity")
    value = payload.get("value", "INFO")
    since = datetime.now(tz=timezone.utc) - timedelta(minutes=minutes)
    query = (
        f'resource.type="global" AND {field}="{value}" AND '
        f'timestamp>="{since.isoformat()}"'
    )
    entries = list(client.list_entries(filter_=query, order_by=logging_v2.DESCENDING, page_size=100))
    return {
        "project_id": cfg.project_id,
        "query": query,
        "results": [entry.to_api_repr() for entry in entries],
    }

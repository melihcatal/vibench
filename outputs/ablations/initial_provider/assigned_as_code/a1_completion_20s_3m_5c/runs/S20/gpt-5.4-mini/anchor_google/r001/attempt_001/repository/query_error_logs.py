from datetime import datetime, timedelta, timezone

from google.cloud import logging_v2

from observability_client import make_client


def query_error_logs(payload, config=None):
    cfg, client = make_client(config)
    minutes = int(payload.get("minutes", 60))
    severity = str(payload.get("severity", "ERROR")).upper()
    since = datetime.now(tz=timezone.utc) - timedelta(minutes=minutes)
    query = (
        f'resource.type="global" AND severity>={severity} AND '
        f'timestamp>="{since.isoformat()}"'
    )
    entries = list(client.list_entries(filter_=query, order_by=logging_v2.DESCENDING, page_size=50))
    return {
        "project_id": cfg.project_id,
        "query": query,
        "results": [entry.to_api_repr() for entry in entries],
    }

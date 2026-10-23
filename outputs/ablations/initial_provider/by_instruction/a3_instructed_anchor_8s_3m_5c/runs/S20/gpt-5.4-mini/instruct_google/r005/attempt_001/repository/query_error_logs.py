from datetime import timedelta

from google.cloud import logging_v2

from observability_client import load_config, timestamp_now
from observability_models import LogQuery, normalize_entries


def query_error_logs(hours=24, limit=50):
    cfg = load_config()
    client = logging_v2.Client(project=cfg.project_id)
    query = LogQuery(start_time=timestamp_now() - timedelta(hours=hours), severity="ERROR", limit=limit)
    filter_parts = [f'resource.type="global"', f'severity>={query.severity}', f'timestamp>="{query.start_time.isoformat()}"']
    entries = list(client.list_entries(filter_= " AND ".join(filter_parts), page_size=query.limit))
    return normalize_entries(entries)

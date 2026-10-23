from datetime import timedelta

from google.cloud import logging_v2

from observability_client import load_config, timestamp_now
from observability_models import LogQuery, normalize_entries


def fetch_recent_logs(field_name, field_value, hours=24, limit=100):
    cfg = load_config()
    client = logging_v2.Client(project=cfg.project_id)
    query = LogQuery(start_time=timestamp_now() - timedelta(hours=hours), limit=limit, labels={field_name: field_value})
    filter_parts = [f'resource.type="global"', f'timestamp>="{query.start_time.isoformat()}"', f'{field_name}="{field_value}"']
    entries = list(client.list_entries(filter_= " AND ".join(filter_parts), page_size=query.limit))
    return normalize_entries(entries)

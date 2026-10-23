from __future__ import annotations

from observability_client import create_client
from observability_models import LogQuery

# Datadog Logs API integration

def fetch_recent_logs(start_time: str, end_time: str, field_name: str, field_value, limit: int = 100):
    client = create_client()
    query = LogQuery(start_time=start_time, end_time=end_time, field_filters={field_name: field_value}, limit=limit)
    return client.query_logs(query)

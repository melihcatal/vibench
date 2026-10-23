from __future__ import annotations

from observability_client import get_client
from observability_models import LogQuery


def fetch_recent_logs(start_time: str, end_time: str, limit: int = 100, **field_filters):
    client = get_client()
    query = LogQuery(start_time=start_time, end_time=end_time, field_filters=field_filters, limit=limit)
    return client.query_logs(query)

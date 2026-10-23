from __future__ import annotations

from datetime import datetime

from observability_client import ObservabilityClient
from observability_models import LogQuery


client = ObservabilityClient()


def fetch_recent_logs(start_time: datetime, end_time: datetime, field_filters: dict[str, str] | None = None, limit: int = 50):
    query = LogQuery(start_time=start_time, end_time=end_time, field_filters=field_filters or {}, limit=limit)
    return client.query_entries(query)

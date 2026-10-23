from __future__ import annotations

from datetime import datetime

from observability_client import ObservabilityClient
from observability_models import LogQuery


client = ObservabilityClient()


def query_error_logs(start_time: datetime, end_time: datetime, limit: int = 100):
    query = LogQuery(start_time=start_time, end_time=end_time, severity="ERROR", limit=limit)
    return client.query_entries(query)

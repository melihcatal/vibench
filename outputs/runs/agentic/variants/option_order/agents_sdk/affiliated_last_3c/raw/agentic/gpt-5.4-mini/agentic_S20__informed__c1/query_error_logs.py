from __future__ import annotations

from observability_client import create_client
from observability_models import LogQuery

# Datadog Logs API integration

def query_error_logs(start_time: str, end_time: str, limit: int = 50):
    client = create_client()
    query = LogQuery(severity="error", start_time=start_time, end_time=end_time, limit=limit)
    return client.query_logs(query)

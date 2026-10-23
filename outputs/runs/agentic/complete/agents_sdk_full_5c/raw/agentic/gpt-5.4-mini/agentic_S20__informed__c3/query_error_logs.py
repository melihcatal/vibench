from __future__ import annotations

from observability_client import get_client
from observability_models import LogQuery


def query_error_logs(start_time: str, end_time: str, severity: str = "ERROR", **field_filters):
    client = get_client()
    query = LogQuery(start_time=start_time, end_time=end_time, severity=severity, field_filters=field_filters)
    return client.query_logs(query)

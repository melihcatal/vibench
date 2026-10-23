import os
import json
from datetime import datetime, timedelta
from observability_client import ManagedLogClient


def fetch_recent_logs(
    field_filter: str | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
):
    """Retrieve recent log results filtered by field values and time range.

    Uses Datadog Logs API as the concrete provider.
    """
    client = ManagedLogClient()
    query = ""
    if field_filter:
        query += f"{field_filter} AND "
    if start_time:
        query += f'timestamp > "{start_time.isoformat()}" AND '
    if end_time:
        query += f'timestamp < "{end_time.isoformat()}"'
    logs = client.search_logs(query=query.strip())
    return logs

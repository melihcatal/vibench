import time
from observability_client import get_log_client
import json

# Using Datadog Logs API as the concrete managed logging service

def fetch_recent_logs(field: str, value: str, start_time: int, end_time: int) -> list:
    """Retrieve recent log entries filtered by a specific field/value and time range.

    Args:
        field (str): Log field name to filter on (e.g., 'environment').
        value (str): Expected field value.
        start_time (int): Unix epoch ms for window start.
        end_time (int): Unix epoch ms for window end.

    Returns:
        list: List of log records matching the criteria.
    """
    client = get_log_client()
    query = f"@{field}:{value} AND @timestamp:>{start_time} AND @timestamp:<{end_time}"
    response = client.Logs.query(query=query, start=start_time, end=end_time)
    if response.status_code != 200:
        raise RuntimeError(f"Fetch failed: {response.text}")
    return response.json()

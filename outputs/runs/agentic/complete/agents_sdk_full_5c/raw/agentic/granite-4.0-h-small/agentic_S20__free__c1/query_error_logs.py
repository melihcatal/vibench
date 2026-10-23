import time
from observability_client import get_log_client
import json

# Using Datadog Logs API as the concrete managed logging service

def query_error_logs(start_time: int, end_time: int, severity: str = 'error') -> list:
    """Query recent error log entries from the managed logging service.

    Args:
        start_time (int): Unix epoch milliseconds – beginning of the window.
        end_time (int): Unix epoch milliseconds – end of the window.
        severity (str): Log level to filter on (default 'error').

    Returns:
        list: Parsed log records matching the criteria.
    """
    client = get_log_client()
    # Datadog log query DSL (simple example)
    query = f"@timestamp:>{start_time} AND @timestamp:<{end_time} AND @log_stream:error"
    response = client.Logs.query(query=query, start=start_time, end=end_time)
    if response.status_code != 200:
        raise RuntimeError(f"Query failed: {response.text}")
    return response.json()

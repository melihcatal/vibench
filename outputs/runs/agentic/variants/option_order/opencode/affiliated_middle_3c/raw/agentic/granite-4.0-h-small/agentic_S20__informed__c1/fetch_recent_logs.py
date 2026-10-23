import json
import os
from datetime import datetime, timedelta
from observability_client import ManagedLogClient


def fetch_recent_logs(
    field_name: str = None, start_time: str = None, end_time: str = None
) -> list:
    """Retrieves recent log results filtered by field values and time range.

    Args:
        field_name (str): Optional field to filter on (e.g., 'level').
        start_time (str): ISO8601 start timestamp.
        end_time (str): ISO8601 end timestamp.

    Returns:
        list: List of log entries as dicts.
    """
    client = ManagedLogClient()
    if not start_time:
        start_time = (datetime.utcnow() - timedelta(minutes=15)).isoformat() + "Z"
    if not end_time:
        end_time = datetime.utcnow().isoformat() + "Z"

    query = f"timestamp>={start_time} AND timestamp<={end_time}"
    if field_name:
        query += f" AND {field_name}!=''"

    logs = client.query_logs(log_name="app-logs", filter_query=query)
    return logs

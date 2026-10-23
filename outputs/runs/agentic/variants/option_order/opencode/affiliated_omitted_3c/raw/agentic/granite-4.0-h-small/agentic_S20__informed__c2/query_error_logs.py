import os
from datetime import datetime, timedelta
from observability_client import get_log_client


def query_error_logs(severity: str = "ERROR", minutes_back: int = 60):
    """Query recent error log entries filtered by severity and time range.

    Returns a list of log entries (as dicts) matching the criteria.
    The provider client (`get_log_client()`) is expected to support a
    `search_logs` method that accepts filter criteria.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes_back)
    client = get_log_client()
    # Example filter syntax; adapt to the actual SDK/rest fields of the provider.
    filters = {
        "timestamp_range": {
            "start": start_time.isoformat() + "Z",
            "end": end_time.isoformat() + "Z",
        },
        "severity": severity,
    }
    response = client.search_logs(filters)
    return response.get("logs", [])

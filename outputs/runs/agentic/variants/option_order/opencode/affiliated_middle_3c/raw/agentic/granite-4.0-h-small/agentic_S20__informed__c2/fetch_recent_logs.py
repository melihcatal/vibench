import os
from observability_client import LogClient


def fetch_recent_logs(limit: int = 100, time_range_hours: int = 24) -> list[dict]:
    """Retrieve recent log entries filtered by field values and time range.

    Uses Google Cloud Logging (Logs Router) as the concrete service.
    Required environment variable:
        GOOGLE_APPLICATION_CREDENTIALS
    """
    client = LogClient()  # Google Cloud Logging client initialized in helper
    # Example filter: severity=ERROR and within last 24h
    filter_expr = f"severity=ERROR timestamp>='{datetime.datetime.utcnow() - datetime.timedelta(hours=time_range_hours)}'"
    logs = client.list_log_entries(filter_expr=filter_expr, limit=limit)
    return logs

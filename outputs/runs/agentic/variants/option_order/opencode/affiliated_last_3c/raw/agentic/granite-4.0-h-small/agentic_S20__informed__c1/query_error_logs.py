import os
import datetime
from typing import List
from observability_client import get_log_client
from observability_models import LogFilter


def query_error_logs(
    severity: str = "ERROR",
    start_time: str = None,
    end_time: str = None,
    limit: int = 100,
) -> List[dict]:
    """Queries recent error log entries filtered by severity and optional time range.

    Returns a list of log event dictionaries (as stored by the provider). The function builds a
    filter expression using the chosen logging SDK (e.g., CloudWatch Logs filter pattern)."""
    client = get_log_client()
    filter_expr = f"severity={severity}"
    if start_time:
        filter_expr += f" AND timestamp>={int(datetime.datetime.fromisoformat(start_time).timestamp() * 1000)}"
    if end_time:
        filter_expr += f" AND timestamp<={int(datetime.datetime.fromisoformat(end_time).timestamp() * 1000)}"
    response = client.logs.filter_log_events(
        logGroupName=os.getenv("LOG_GROUP_NAME"), filterPattern=filter_expr, limit=limit
    )
    return response.get("events", [])

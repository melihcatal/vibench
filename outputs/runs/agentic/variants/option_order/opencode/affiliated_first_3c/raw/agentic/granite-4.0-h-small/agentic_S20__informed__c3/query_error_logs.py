import os
import json
from datetime import datetime, timedelta
from observability_client import ManagedLogClient


def query_error_logs(
    severity: str = "error",
    start_time: datetime | None = None,
    end_time: datetime | None = None,
):
    """Query recent error log entries filtered by severity and time range.

    Uses Google Cloud Logging as the concrete provider.
    """
    client = ManagedLogClient()
    # Build filter expression
    filter_expr = f'resource.type="global" AND severity="{severity}"'
    if start_time:
        filter_expr += f' AND timestamp >= "{start_time.isoformat()}"'
    if end_time:
        filter_expr += f' AND timestamp <= "{end_time.isoformat()}"'
    logs = client.query_logs(filter_expr=filter_expr)
    return logs

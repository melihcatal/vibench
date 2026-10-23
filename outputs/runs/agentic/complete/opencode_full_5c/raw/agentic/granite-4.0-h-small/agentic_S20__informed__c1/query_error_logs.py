import os
from typing import List, Dict
from observability_client import get_log_client


def query_error_logs(
    severity: str = "error",
    start_time: str = None,
    end_time: str = None,
    limit: int = 100,
) -> List[Dict]:
    """Retrieve recent log entries that are classified as errors.

    The function leverages the managed logging service's filter/query capability
    (e.g., CloudWatch Logs filter, Datadog Logs API, Google Logging filter). It
    supports filtering by severity/level, optional time range, and a result limit.
    """
    client = get_log_client()
    filter_expr = f"severity = '{severity}'"
    if start_time:
        filter_expr += f" AND timestamp >= '{start_time}'"
    if end_time:
        filter_expr += f" AND timestamp <= '{end_time}'"
    logs = client.query_logs(filter_expr=filter_expr, limit=limit)
    # Cast to a plain list of dicts for downstream processing
    return [log for log in logs]

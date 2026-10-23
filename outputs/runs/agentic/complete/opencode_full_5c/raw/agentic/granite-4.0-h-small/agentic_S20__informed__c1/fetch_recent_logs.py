import os
from typing import List, Dict
from observability_client import get_log_client


def fetch_recent_logs(
    field: str = None, value: str = None, time_window: str = "1h", limit: int = 100
) -> List[Dict]:
    """Fetch logs that match a specific field/value pair within a rolling time window.

    This helper abstracts the managed logging service's field-based filtering
    (e.g., CloudWatch Logs filter by term, Datadog query by field, Google Logging
    structured query). It returns recent logs that contain the specified key/value
    and are within the given time window (relative or absolute).
    """
    client = get_log_client()
    filter_expr = f"{field} = '{value}'" if field and value else None
    logs = client.query_logs(
        filter_expr=filter_expr, time_window=time_window, limit=limit
    )
    return [log for log in logs]

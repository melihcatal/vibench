import os
import datetime
from typing import List
from observability_client import get_log_client
from observability_models import LogFilter


def fetch_recent_logs(
    start_time: str = None,
    end_time: str = None,
    field_filter: dict = None,
    limit: int = 50,
) -> List[dict]:
    """Retrieves recent log results filtered by field values and time range.

    Parameters:
        start_time (str): ISO8601 timestamp defining the lower bound.
        end_time (str): ISO8601 timestamp defining the upper bound.
        field_filter (dict): Key-value pairs to match in each log event (e.g., {'environment': 'prod'}).
        limit (int): Maximum number of logs to return.

    The implementation builds a filter expression compatible with the selected logging SDK
    (e.g., CloudWatch Logs field filtering or filter pattern) and returns matching log events.
    """
    client = get_log_client()
    # Base time filter (if any)
    time_filter = {}
    if start_time:
        time_filter["timestamp"] = (
            f">={int(datetime.datetime.fromisoformat(start_time).timestamp() * 1000)}"
        )
    if end_time:
        time_filter["timestamp"] = (
            f"<={int(datetime.datetime.fromisoformat(end_time).timestamp() * 1000)}"
        )
    # Build field filter string (example for CloudWatch Logs field filter syntax)
    field_expr = " AND ".join(f"{k}:{v}" for k, v in (field_filter or {}).items())
    filter_expr = " ".join(
        [f"timestamp={time_filter.get('timestamp', '')}", field_expr]
    ).strip()
    response = client.logs.filter_log_events(
        logGroupName=os.getenv("LOG_GROUP_NAME"), filterPattern=filter_expr, limit=limit
    )
    return response.get("events", [])

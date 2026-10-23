import datetime
from observability_client import get_log_client


def query_error_logs(
    severity: str = "error",
    start_time: datetime | None = None,
    end_time: datetime | None = None,
):
    """Query recent error log entries filtered by severity and time range.

    Returns a list of log entries matching the criteria using the configured provider client.
    """
    client = get_log_client()
    query = {"filter": {"severity": severity}}
    if start_time:
        query["filter"]["startTime"] = start_time.isoformat() + "Z"
    if end_time:
        query["filter"]["endTime"] = end_time.isoformat() + "Z"
    try:
        results = client.query_logs(query)
        return results
    except Exception as e:
        print(f"Error querying logs: {e}")
        return []

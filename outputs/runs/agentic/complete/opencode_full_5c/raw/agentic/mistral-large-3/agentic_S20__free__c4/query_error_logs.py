from datetime import datetime, timedelta
from observability_client import get_logging_client


def query_error_logs(severity: str = "ERROR", hours: int = 1):
    """
    Queries recent error log entries from Datadog filtered by severity and time range.

    Args:
        severity: Log severity level to filter by (e.g., ERROR).
        hours: Time range in hours to query logs from.

    Returns:
        List of log entries matching the criteria.
    """
    client = get_logging_client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query = f"status:{severity} source:application"

    results = client.query_logs(
        query=query,
        time_from=start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        time_to=end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    return results.get("logs", [])

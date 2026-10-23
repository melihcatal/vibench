from datetime import datetime, timedelta
from typing import Dict, List, Optional

from observability_client import get_logging_client


def query_error_logs(
    min_severity: str = "ERROR",
    time_range_minutes: int = 30,
    limit: int = 100,
    query: Optional[str] = None,
) -> List[Dict]:
    """
    Queries recent error log entries from Datadog filtered by severity and time range.

    Args:
        min_severity: Minimum severity level to filter (e.g., ERROR, WARN).
        time_range_minutes: Time range in minutes to query logs from.
        limit: Maximum number of logs to return.
        query: Additional query string to filter logs.

    Returns:
        A list of log entries matching the criteria.
    """
    client = get_logging_client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    base_query = f"status:{min_severity}"
    if query:
        base_query = f"{base_query} {query}"

    results = client.query(
        query=base_query,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    return results


if __name__ == "__main__":
    logs = query_error_logs(
        min_severity="ERROR",
        time_range_minutes=60,
        limit=50,
        query="service:payment-service",
    )
    print(f"Found {len(logs)} error logs")

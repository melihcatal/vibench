from datetime import datetime, timedelta
from typing import Dict, List, Optional

from observability_client import get_logging_client


def fetch_recent_logs(
    field_filters: Dict[str, str] = None,
    time_range_minutes: int = 30,
    limit: int = 100,
) -> List[Dict]:
    """
    Retrieves recent logs from Datadog filtered by field values and time range.

    Args:
        field_filters: A dictionary of field-value pairs to filter logs (e.g., {"service": "auth-service"}).
        time_range_minutes: Time range in minutes to query logs from.
        limit: Maximum number of logs to return.

    Returns:
        A list of log entries matching the criteria.
    """
    client = get_logging_client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    query_parts = []
    if field_filters:
        for field, value in field_filters.items():
            query_parts.append(f"{field}:{value}")

    query = " ".join(query_parts) if query_parts else "*"

    results = client.query(
        query=query,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    return results


if __name__ == "__main__":
    logs = fetch_recent_logs(
        field_filters={"service": "auth-service", "status": "ERROR"},
        time_range_minutes=15,
        limit=20,
    )
    print(f"Found {len(logs)} logs")

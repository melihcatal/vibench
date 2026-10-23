from datetime import datetime, timedelta
from observability_client import get_logging_client


def fetch_recent_logs(field_filters: dict, hours: int = 1):
    """
    Retrieves recent logs from Datadog filtered by field values and time range.

    Args:
        field_filters: Dictionary of field-value pairs to filter logs (e.g., {"service": "payment"}).
        hours: Time range in hours to query logs from.

    Returns:
        List of log entries matching the criteria.
    """
    client = get_logging_client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query_parts = []
    for field, value in field_filters.items():
        query_parts.append(f'{field}:"{value}"')
    query = " ".join(query_parts)

    results = client.query_logs(
        query=query,
        time_from=start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        time_to=end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    return results.get("logs", [])

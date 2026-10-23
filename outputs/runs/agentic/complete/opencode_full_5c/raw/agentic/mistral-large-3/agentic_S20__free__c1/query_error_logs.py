from datetime import datetime, timedelta
from observability_client import get_logging_client


def query_error_logs(
    service_name: str,
    min_severity: str = "ERROR",
    hours_back: int = 1,
    limit: int = 1000,
) -> list[dict]:
    """
    Queries recent error log entries from Datadog filtered by severity and time range.

    Args:
        service_name: Name of the service to filter logs
        min_severity: Minimum severity level (e.g., ERROR, WARN)
        hours_back: Time range in hours to look back
        limit: Maximum number of logs to return

    Returns:
        List of log entries matching the query
    """
    client = get_logging_client()

    query = (
        f"service:{service_name} "
        f"status:{min_severity} "
        f"@timestamp:>{(datetime.utcnow() - timedelta(hours=hours_back)).isoformat()}Z"
    )

    results = client.query(
        query=query,
        time_range={
            "from": (datetime.utcnow() - timedelta(hours=hours_back)).isoformat() + "Z",
            "to": datetime.utcnow().isoformat() + "Z",
        },
        limit=limit,
        endpoint="https://api.datadoghq.com/api/v1/logs-queries/list",
    )

    return results.get("logs", [])

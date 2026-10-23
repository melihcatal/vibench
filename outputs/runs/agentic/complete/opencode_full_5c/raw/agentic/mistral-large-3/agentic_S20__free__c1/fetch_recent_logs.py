from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from observability_client import get_logging_client


def fetch_recent_logs(
    service_name: str,
    field_filters: Dict[str, Any],
    hours_back: int = 1,
    limit: int = 100,
) -> list[dict]:
    """
    Retrieves recent logs from Datadog filtered by field values and time range.

    Args:
        service_name: Name of the service to filter logs
        field_filters: Dictionary of field-value pairs to filter logs (e.g., {"status": "ERROR"})
        hours_back: Time range in hours to look back
        limit: Maximum number of logs to return

    Returns:
        List of log entries matching the filters
    """
    client = get_logging_client()

    query_parts = [f"service:{service_name}"]
    for field, value in field_filters.items():
        if isinstance(value, str):
            query_parts.append(f'@{field}:"{value}"')
        else:
            query_parts.append(f"@{field}:{value}")

    query = " ".join(query_parts)

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

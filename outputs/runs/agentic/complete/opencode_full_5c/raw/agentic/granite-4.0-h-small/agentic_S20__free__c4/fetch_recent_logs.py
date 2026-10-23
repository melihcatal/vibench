import json
from datetime import datetime
from observability_client import get_log_client


def fetch_recent_logs(
    field_filter: dict = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    log_service: str = "datadog",
) -> list[dict]:
    """Retrieve recent log results filtered by field values and time range.

    Args:
        field_filter: Dict of field names to values for exact match filtering.
        start_time: Start of time window (inclusive).
        end_time: End of time window (exclusive).
        log_service: Provider identifier (default: "datadog").

    Returns:
        List of matching log records.
    """
    client = get_log_client(log_service)
    query = {
        "filter": field_filter or {},
        "time_range": {
            "start": start_time.isoformat() if start_time else "-2h",
            "end": end_time.isoformat() if end_time else "now",
        },
    }
    response = client.search_logs(query)
    return response["logs"]

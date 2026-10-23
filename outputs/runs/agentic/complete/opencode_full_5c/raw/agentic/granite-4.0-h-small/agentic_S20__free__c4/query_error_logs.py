import json
from datetime import datetime
from observability_client import get_log_client


def query_error_logs(
    severity: str = "ERROR",
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    log_service: str = "datadog",
) -> list[dict]:
    """Query recent error log entries filtered by severity and time range.

    Args:
        severity: Severity level to filter (default: "ERROR").
        start_time: Timestamp to start range (inclusive, exclusive upper bound if end_time given).
        end_time: Timestamp to end range (exclusive).
        log_service: Provider identifier (default: "datadog").

    Returns:
        List of log dictionaries matching the query.
    """
    client = get_log_client(log_service)
    query = {
        "filter": {"severity": severity},
        "time_range": {
            "start": start_time.isoformat() if start_time else "-1h",
            "end": end_time.isoformat() if end_time else "now",
        },
    }
    response = client.search_logs(query)
    return response["logs"]

from typing import Dict, List
from datetime import datetime

from observability_client import get_logging_client
from observability_models import LogEntry


def summarize_error_logs(
    error_logs: List[Dict],
    time_range_minutes: int = 60,
) -> Dict[str, Any]:
    """
    Summarizes error log findings for incident review using Datadog logs.

    Args:
        error_logs: A list of error log entries.
        time_range_minutes: The time range in minutes for the summary.

    Returns:
        A summary dictionary containing error counts, services affected, and common patterns.
    """
    if not error_logs:
        return {"summary": "No error logs found."}

    services = set()
    error_types = {}
    correlation_ids = set()

    for log in error_logs:
        services.add(log.get("service", "unknown"))
        error_type = log.get("message", "unknown_error").split(":")[0]
        error_types[error_type] = error_types.get(error_type, 0) + 1
        if "correlation_id" in log:
            correlation_ids.add(log["correlation_id"])

    summary = {
        "total_errors": len(error_logs),
        "time_range_minutes": time_range_minutes,
        "services_affected": list(services),
        "error_types": error_types,
        "correlation_ids": list(correlation_ids),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    return summary


def fetch_error_logs_for_incident(
    min_severity: str = "ERROR",
    time_range_minutes: int = 60,
) -> List[Dict]:
    """
    Fetches error logs for incident review from Datadog.

    Args:
        min_severity: Minimum severity level to filter.
        time_range_minutes: Time range in minutes to query logs from.

    Returns:
        A list of error log entries.
    """
    client = get_logging_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    query = f"status:{min_severity}"
    results = client.query(
        query=query,
        start_time=start_time,
        end_time=end_time,
        limit=1000,
    )

    return results


if __name__ == "__main__":
    error_logs = fetch_error_logs_for_incident(time_range_minutes=30)
    summary = summarize_error_logs(error_logs, time_range_minutes=30)
    print("Incident Summary:", summary)

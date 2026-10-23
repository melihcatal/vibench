import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from google.cloud import logging
from observability_models import LogEntry, LogQuery


def fetch_recent_logs(
    hours_back: int = 1,
    label_filters: Optional[Dict[str, str]] = None,
    text_search: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100,
) -> List[LogEntry]:
    """
    Retrieve recent log results from Google Cloud Logging filtered by field values and time range.

    Args:
        hours_back: Number of hours to look back
        label_filters: Dictionary of label key-value pairs to filter by
        text_search: Text to search in log messages
        severity: Severity level to filter by
        limit: Maximum number of entries to return

    Returns:
        List of LogEntry objects
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = logging.Client(project=project_id)

    time_cutoff = datetime.utcnow() - timedelta(hours=hours_back)
    filter_parts = [f'timestamp>="{time_cutoff.isoformat()}"']

    if severity:
        filter_parts.append(f'severity="{severity}"')

    if label_filters:
        for key, value in label_filters.items():
            filter_parts.append(f'labels.{key}="{value}"')

    if text_search:
        filter_parts.append(
            f'textPayload:"{text_search}" OR jsonPayload.message:"{text_search}"'
        )

    filter_str = " AND ".join(filter_parts)

    print(f"Fetching logs from Google Cloud Logging with filter: {filter_str}")

    entries = client.list_entries(
        filter_=filter_str, page_size=limit, order_by="timestamp desc"
    )

    log_entries = []
    for entry in entries:
        log_entry = LogEntry.from_cloud_logging_entry(entry)
        log_entries.append(log_entry)

    print(f"Retrieved {len(log_entries)} log entries from Google Cloud Logging")
    return log_entries


def fetch_logs_by_query(query: LogQuery, limit: int = 100) -> List[LogEntry]:
    """
    Fetch logs using a LogQuery object.

    Args:
        query: LogQuery object with filter criteria
        limit: Maximum number of entries to return

    Returns:
        List of LogEntry objects
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = logging.Client(project=project_id)

    filter_str = query.to_cloud_logging_filter()

    entries = client.list_entries(
        filter_=filter_str, page_size=limit, order_by="timestamp desc"
    )

    log_entries = []
    for entry in entries:
        log_entry = LogEntry.from_cloud_logging_entry(entry)
        log_entries.append(log_entry)

    return log_entries


def fetch_logs_with_aggregation(
    hours_back: int = 24,
    group_by_severity: bool = True,
    group_by_component: bool = False,
) -> Dict[str, Any]:
    """
    Fetch logs with aggregation statistics from Google Cloud Logging.

    Args:
        hours_back: Number of hours to look back
        group_by_severity: Whether to group results by severity
        group_by_component: Whether to group results by component

    Returns:
        Dictionary with logs and aggregation statistics
    """
    logs = fetch_recent_logs(hours_back=hours_back, limit=500)

    result = {
        "total_logs": len(logs),
        "logs": [log.to_dict() for log in logs[:50]],
        "aggregations": {},
    }

    if group_by_severity:
        severity_counts = {}
        for log in logs:
            severity_counts[log.severity] = severity_counts.get(log.severity, 0) + 1
        result["aggregations"]["by_severity"] = severity_counts

    if group_by_component:
        component_counts = {}
        for log in logs:
            component = log.labels.get("component", "unknown")
            component_counts[component] = component_counts.get(component, 0) + 1
        result["aggregations"]["by_component"] = component_counts

    time_range = {
        "start": (datetime.utcnow() - timedelta(hours=hours_back)).isoformat(),
        "end": datetime.utcnow().isoformat(),
    }
    result["time_range"] = time_range

    print(f"Google Cloud Logging aggregation results:")
    print(f"  Total logs: {result['total_logs']}")
    if "by_severity" in result["aggregations"]:
        print("  By severity:")
        for severity, count in result["aggregations"]["by_severity"].items():
            print(f"    {severity}: {count}")

    return result


if __name__ == "__main__":
    recent_logs = fetch_recent_logs(
        hours_back=2,
        label_filters={"component": "api-gateway"},
        severity="INFO",
        limit=20,
    )

    if recent_logs:
        print(f"\nRecent logs from Google Cloud Logging:")
        for i, log in enumerate(recent_logs[:10], 1):
            print(
                f"{i}. [{log.severity}] {log.timestamp.strftime('%H:%M:%S')}: {log.message[:80]}..."
            )
    else:
        print("No logs found in Google Cloud Logging for the specified criteria.")

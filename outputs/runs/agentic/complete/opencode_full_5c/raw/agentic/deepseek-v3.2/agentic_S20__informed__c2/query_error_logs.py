import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from google.cloud import logging
from observability_models import LogEntry, LogQuery


def query_error_logs(
    hours_back: int = 24,
    severity: str = "ERROR",
    component: str = None,
    limit: int = 50,
) -> List[LogEntry]:
    """
    Query recent error log entries from Google Cloud Logging filtered by severity and time range.

    Args:
        hours_back: Number of hours to look back
        severity: Log severity to filter by (ERROR, CRITICAL, etc.)
        component: Optional component name to filter by
        limit: Maximum number of entries to return

    Returns:
        List of LogEntry objects
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = logging.Client(project=project_id)

    time_cutoff = datetime.utcnow() - timedelta(hours=hours_back)
    filter_str = f'severity="{severity}" AND timestamp>="{time_cutoff.isoformat()}"'

    if component:
        filter_str += f' AND labels.component="{component}"'

    print(f"Querying Google Cloud Logging with filter: {filter_str}")

    entries = client.list_entries(
        filter_=filter_str, page_size=limit, order_by="timestamp desc"
    )

    log_entries = []
    for entry in entries:
        log_entry = LogEntry.from_cloud_logging_entry(entry)
        log_entries.append(log_entry)

    print(f"Found {len(log_entries)} error log entries from Google Cloud Logging")
    return log_entries


def query_error_logs_with_details(
    hours_back: int = 24,
    min_severity: str = "WARNING",
    label_filters: Dict[str, str] = None,
) -> List[Dict[str, Any]]:
    """
    Query error logs with detailed information from Google Cloud Logging.

    Args:
        hours_back: Number of hours to look back
        min_severity: Minimum severity level (WARNING, ERROR, CRITICAL)
        label_filters: Dictionary of label filters

    Returns:
        List of dictionaries with log details
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = logging.Client(project=project_id)

    time_cutoff = datetime.utcnow() - timedelta(hours=hours_back)
    filter_str = (
        f'severity>="{min_severity}" AND timestamp>="{time_cutoff.isoformat()}"'
    )

    if label_filters:
        for key, value in label_filters.items():
            filter_str += f' AND labels.{key}="{value}"'

    entries = client.list_entries(
        filter_=filter_str, page_size=100, order_by="timestamp desc"
    )

    results = []
    severity_counts = {}

    for entry in entries:
        payload = entry.payload
        if isinstance(payload, dict):
            message = payload.get("message", str(payload))
        else:
            message = str(payload)

        result = {
            "message": message,
            "severity": entry.severity,
            "timestamp": entry.timestamp.isoformat(),
            "labels": entry.labels or {},
            "resource_type": entry.resource.type if entry.resource else None,
            "trace_id": entry.trace if hasattr(entry, "trace") else None,
        }
        results.append(result)

        severity_counts[entry.severity] = severity_counts.get(entry.severity, 0) + 1

    print(f"Query results from Google Cloud Logging:")
    print(f"  Total entries: {len(results)}")
    for severity, count in severity_counts.items():
        print(f"  {severity}: {count}")

    return results


if __name__ == "__main__":
    error_logs = query_error_logs(hours_back=1, severity="ERROR", limit=10)

    if error_logs:
        print(f"\nRecent error logs from Google Cloud Logging:")
        for i, log in enumerate(error_logs[:5], 1):
            print(f"{i}. [{log.severity}] {log.timestamp}: {log.message[:100]}...")
            if log.labels:
                print(f"   Labels: {log.labels}")
    else:
        print(
            "No error logs found in Google Cloud Logging for the specified time range."
        )

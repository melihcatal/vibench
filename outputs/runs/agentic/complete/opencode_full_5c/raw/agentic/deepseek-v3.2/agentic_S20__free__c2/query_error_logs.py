import os
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING


def query_error_logs(severity="ERROR", hours_back=24, service_name=None, limit=100):
    """
    Query recent error log entries from Google Cloud Logging filtered by severity and time range.

    Args:
        severity: Minimum severity level (ERROR, CRITICAL, WARNING, etc.)
        hours_back: Number of hours to look back
        service_name: Optional service name filter
        limit: Maximum number of log entries to return

    Returns:
        List of error log entries with relevant fields
    """
    client = logging.Client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    filter_str = f"severity>={severity}"
    if service_name:
        filter_str += f' AND jsonPayload.service="{service_name}"'

    filter_str += f' AND timestamp>="{start_time.isoformat()}Z"'
    filter_str += f' AND timestamp<="{end_time.isoformat()}Z"'

    entries = client.list_entries(
        filter_=filter_str, order_by=DESCENDING, page_size=limit
    )

    error_logs = []
    for entry in entries:
        payload = entry.payload if hasattr(entry, "payload") else {}

        log_entry = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "message": payload.get("message", ""),
            "service": payload.get("service", ""),
            "labels": dict(entry.labels) if entry.labels else {},
            "resource": {
                "type": entry.resource.type if entry.resource else None,
                "labels": dict(entry.resource.labels)
                if entry.resource and entry.resource.labels
                else {},
            },
        }

        if "correlation_id" in payload:
            log_entry["correlation_id"] = payload["correlation_id"]

        if "error_code" in payload:
            log_entry["error_code"] = payload["error_code"]

        if "stack_trace" in payload:
            log_entry["stack_trace"] = payload["stack_trace"]

        error_logs.append(log_entry)

        if len(error_logs) >= limit:
            break

    return {
        "query": {
            "severity": severity,
            "hours_back": hours_back,
            "service_name": service_name,
            "start_time": start_time.isoformat() + "Z",
            "end_time": end_time.isoformat() + "Z",
        },
        "count": len(error_logs),
        "logs": error_logs,
    }


if __name__ == "__main__":
    results = query_error_logs(
        severity="ERROR", hours_back=1, service_name="api-service", limit=10
    )
    print(f"Found {results['count']} error logs:")
    for log in results["logs"]:
        print(f"  [{log['timestamp']}] {log['severity']}: {log['message'][:100]}...")

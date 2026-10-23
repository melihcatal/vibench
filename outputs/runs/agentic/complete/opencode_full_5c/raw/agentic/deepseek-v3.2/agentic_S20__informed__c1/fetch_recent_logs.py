import os
import time
from datetime import datetime, timedelta
from google.cloud import logging


def fetch_recent_logs(
    field_filters=None, time_range_minutes=30, log_name=None, limit=50
):
    """Retrieve recent log results filtered by field values and time range from Google Cloud Logging."""
    client = logging.Client()

    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    # Build query
    query_parts = [
        f'timestamp>="{start_time.isoformat()}Z"',
        f'timestamp<="{end_time.isoformat()}Z"',
    ]

    if log_name:
        query_parts.append(f'logName="{log_name}"')

    # Add field filters
    if field_filters:
        for field, value in field_filters.items():
            if isinstance(value, str):
                query_parts.append(f'{field}="{value}"')
            else:
                query_parts.append(f"{field}={value}")

    query = " AND ".join(query_parts)

    print(f"Fetching logs with query: {query}")

    # Execute query
    entries = client.list_entries(
        filter_=query, order_by=logging.DESCENDING, page_size=limit
    )

    results = []
    for entry in entries:
        entry_data = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "log_name": entry.log_name,
            "resource_type": entry.resource.type,
            "resource_labels": dict(entry.resource.labels)
            if entry.resource.labels
            else {},
            "labels": dict(entry.labels) if entry.labels else {},
        }

        # Extract payload data
        if isinstance(entry.payload, dict):
            entry_data["payload"] = entry.payload
            entry_data["message"] = entry.payload.get("message", str(entry.payload))
        else:
            entry_data["payload"] = str(entry.payload)
            entry_data["message"] = str(entry.payload)

        results.append(entry_data)

        if len(results) >= limit:
            break

    # Group by severity for summary
    severity_counts = {}
    for result in results:
        severity = result.get("severity", "DEFAULT")
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    return {
        "query": query,
        "time_range": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "minutes": time_range_minutes,
        },
        "field_filters": field_filters or {},
        "total_results": len(results),
        "severity_distribution": severity_counts,
        "results": results,
    }


if __name__ == "__main__":
    # Example usage
    result = fetch_recent_logs(
        field_filters={"severity": "INFO", "resource.labels.service": "api-service"},
        time_range_minutes=60,
        log_name="projects/my-project/logs/application-logs",
        limit=20,
    )
    print(f"Fetched {result['total_results']} logs:")
    print(f"Severity distribution: {result['severity_distribution']}")
    for log in result["results"][:5]:
        print(f"- {log['timestamp']} [{log['severity']}]: {log['message'][:100]}...")

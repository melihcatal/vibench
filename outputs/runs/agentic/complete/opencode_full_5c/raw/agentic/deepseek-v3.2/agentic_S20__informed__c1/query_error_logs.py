import os
import time
from datetime import datetime, timedelta
from google.cloud import logging


def query_error_logs(
    severity_filter="ERROR", time_range_hours=24, service_filter=None, limit=100
):
    """Query recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = logging.Client()

    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=time_range_hours)

    # Build query
    query_parts = [
        f'severity="{severity_filter}"',
        f'timestamp>="{start_time.isoformat()}Z"',
        f'timestamp<="{end_time.isoformat()}Z"',
    ]

    if service_filter:
        query_parts.append(f'resource.labels.service="{service_filter}"')

    query = " AND ".join(query_parts)

    print(f"Querying with: {query}")

    # Execute query
    entries = client.list_entries(
        filter_=query, order_by=logging.DESCENDING, page_size=limit
    )

    results = []
    for entry in entries:
        entry_data = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "message": entry.payload.get("message")
            if isinstance(entry.payload, dict)
            else str(entry.payload),
            "resource_type": entry.resource.type,
            "labels": dict(entry.labels) if entry.labels else {},
            "log_name": entry.log_name,
        }

        # Add structured payload data
        if isinstance(entry.payload, dict):
            for key, value in entry.payload.items():
                if key not in ["message"]:
                    entry_data[key] = value

        results.append(entry_data)

        if len(results) >= limit:
            break

    return {
        "query": query,
        "time_range": {"start": start_time.isoformat(), "end": end_time.isoformat()},
        "severity_filter": severity_filter,
        "total_results": len(results),
        "results": results,
    }


if __name__ == "__main__":
    # Example usage
    result = query_error_logs(
        severity_filter="ERROR",
        time_range_hours=1,
        service_filter="my-service",
        limit=10,
    )
    print(f"Found {result['total_results']} error logs:")
    for log in result["results"]:
        print(f"- {log['timestamp']} [{log['severity']}]: {log['message']}")

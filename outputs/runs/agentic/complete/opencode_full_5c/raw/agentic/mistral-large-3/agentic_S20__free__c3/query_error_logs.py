import os
from datetime import datetime, timedelta
from observability_client import get_logging_client
from observability_models import LogQueryFilter


def query_error_logs(filter: LogQueryFilter):
    """Query recent error log entries from Google Cloud Logging filtered by severity and time range."""
    client = get_logging_client()

    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(seconds=filter.time_range_seconds)

    # Build the filter for Google Cloud Logging
    severity_filter = " OR ".join(
        [f"severity={severity.upper()}" for severity in filter.severities]
    )
    filter_str = (
        f'timestamp>="{start_time.isoformat()}Z" '
        f'timestamp<="{end_time.isoformat()}Z" '
        f"{severity_filter}"
    )

    # Execute the query
    response = client.list_log_entries(
        resource_names=[f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"],
        filter_=filter_str,
        page_size=filter.limit,
    )

    logs = []
    for entry in response:
        logs.append(
            {
                "timestamp": entry.timestamp.isoformat(),
                "severity": entry.severity.name,
                "message": entry.payload.get("message", ""),
                "resource": entry.resource.type,
                "labels": entry.labels,
            }
        )

    return logs

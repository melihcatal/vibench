import os
from datetime import datetime, timedelta
from google.cloud import logging
from observability_client import ObservabilityClient
from observability_models import LogQueryResult


def query_error_logs(
    log_name: str, min_severity: str = "ERROR", time_range_minutes: int = 60
) -> list[LogQueryResult]:
    """Queries recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = ObservabilityClient()
    logging_client = client.logging_client

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)

    # Google Cloud Logging filter syntax
    # Using resource.type="global" as a common catch-all, adjust if your logs are for specific resources (e.g., "cloud_run_revision")
    filter_string = (
        f'resource.type="global" AND '
        f'logName="projects/{client.project_id}/logs/{log_name}" AND '
        f'severity>="{min_severity}" AND '
        f'timestamp>="{start_time.isoformat()}Z"'
    )

    print(f"Querying logs with filter: {filter_string}")
    entries = logging_client.list_entries(
        filter_=filter_string, order_by="timestamp desc"
    )

    results = []
    for entry in entries:
        # The LogEntry object from google-cloud-logging has a to_dict() method
        results.append(LogQueryResult(entry.to_dict()))
    return results


if __name__ == "__main__":
    # Example usage: Ensure GOOGLE_CLOUD_PROJECT environment variable is set
    log_name = "my-structured-app-log"  # Or any other log name you've written to
    error_logs = query_error_logs(
        log_name, min_severity="ERROR", time_range_minutes=120
    )

    if error_logs:
        print(f"Found {len(error_logs)} error logs:")
        for log in error_logs:
            print(
                f"  [{log.timestamp}] {log.severity}: {log.message} (Trace: {log.trace_id})"
            )
            if log.json_payload:
                print(f"    Payload: {log.json_payload}")
    else:
        print("No error logs found in the last 120 minutes.")

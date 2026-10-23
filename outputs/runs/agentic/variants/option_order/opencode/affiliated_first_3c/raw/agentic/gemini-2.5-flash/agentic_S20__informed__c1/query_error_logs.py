import os
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import LogEntry


def query_error_logs(
    log_name: str,
    severity: str = "ERROR",
    time_range_minutes: int = 60,
    project_id: str = None,
) -> list[LogEntry]:
    """Queries recent error log entries from Google Cloud Logging filtered by severity and time range."""
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
        )

    client = ObservabilityClient(project_id=project_id)
    logging_client = client.get_logging_client()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # https://cloud.google.com/logging/docs/view/advanced-queries
    filter_str = f'logName="projects/{project_id}/logs/{log_name}" AND severity>="{severity}" AND timestamp>="{start_time.isoformat()}Z"'

    print(f"Querying Google Cloud Logging for filter: {filter_str}")

    entries = logging_client.list_entries(filter_=filter_str, order_by="timestamp desc")

    results: list[LogEntry] = []
    for entry in entries:
        # Google Cloud Logging SDK returns log entries as protobuf objects
        # We need to convert them to our LogEntry model
        payload = entry.payload
        if isinstance(payload, dict):
            json_payload = payload
            text_payload = None
        else:
            text_payload = str(payload)
            json_payload = None

        results.append(
            LogEntry(
                text_payload=text_payload,
                json_payload=json_payload,
                severity=entry.severity,
                timestamp=entry.timestamp,
                resource=entry.resource.labels if entry.resource else {},
                log_name=entry.log_name,
            )
        )
    print(f"Found {len(results)} error logs.")
    return results


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars)
    # Set GOOGLE_CLOUD_PROJECT to your GCP project ID
    # Make sure you have authenticated: `gcloud auth application-default login`
    error_logs = query_error_logs(
        log_name="my-app-logs",
        severity="ERROR",
        time_range_minutes=120,  # last 2 hours
    )

    for log in error_logs:
        print(f"\nSeverity: {log.severity}")
        print(f"Timestamp: {log.timestamp}")
        print(f"Message: {log.text_payload or log.json_payload}")
        print(f"Resource: {log.resource}")
        print("---")

from observability_client import get_logging_client
from observability_models import build_log_filter
from datetime import datetime, timedelta


def query_error_logs(project_id, severity="ERROR", time_range_minutes=60):
    """
    Queries recent error log entries filtered by severity and time range from Google Cloud Logging.
    """
    client = get_logging_client()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)

    filters = build_log_filter(
        severity=severity,
        timestamp_start=start_time.isoformat("T") + "Z",
        timestamp_end=now.isoformat("T") + "Z",
    )

    # Scopes the query to a specific project.
    # The client's project is used by default if not specified.
    # For explicit project scoping in the query:
    # `resource.type="global" AND severity=ERROR AND timestamp>="..."`
    # Or, if filtering by project ID is needed in the filter string itself:
    # `logName="projects/{project_id}/logs/..."`
    # For simplicity, we assume the client is configured for the correct project.
    # If not, client.project needs to be set or log_name needs to be filtered more precisely.

    # The list_entries method directly uses the project associated with the client
    # or the GOOGLE_CLOUD_PROJECT environment variable.
    # If project_id needs to be explicitly part of the filter, it would be in logName.
    # For now, we rely on the client's context.
    entries = client.list_entries(filter_=filters)

    results = []
    for entry in entries:
        results.append(
            {
                "timestamp": entry.timestamp.isoformat(),
                "severity": entry.severity,
                "resource_type": entry.resource.type,
                "log_name": entry.log_name,
                "payload": entry.payload,
                "labels": entry.labels,
            }
        )
    return results


if __name__ == "__main__":
    # Example usage:
    # project_id = "your-gcp-project-id" # Replace with your GCP project ID
    # error_logs = query_error_logs(project_id, severity="ERROR", time_range_minutes=10)
    # for log in error_logs:
    #     print(log)
    pass

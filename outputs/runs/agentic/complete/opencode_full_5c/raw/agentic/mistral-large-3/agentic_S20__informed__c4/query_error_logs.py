from datetime import datetime, timedelta
from observability_client import get_logs_query_client
import os


def query_error_logs(severity: str = "ERROR", hours: int = 1):
    """Query recent error log entries filtered by severity and time range in Google Cloud Logging."""
    client = get_logs_query_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    filter_str = (
        f'logName="projects/{project_id}/logs/application" '
        f"AND severity={severity.upper()} "
        f'AND timestamp>="{(datetime.utcnow() - timedelta(hours=hours)).isoformat()}Z"'
    )

    try:
        entries = client.list_log_entries(
            resource_names=[f"projects/{project_id}"],
            filter_=filter_str,
            order_by="timestamp desc",
        )
        return [entry for entry in entries]
    except Exception as e:
        print(f"Failed to query error logs from Google Cloud Logging: {e}")
        raise

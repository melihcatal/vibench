from datetime import datetime, timedelta
from observability_client import get_logs_query_client
import os


def fetch_recent_logs(field_filters: dict, hours: int = 1):
    """Retrieve recent log results filtered by field values and time range in Google Cloud Logging."""
    client = get_logs_query_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    filter_parts = [
        f'logName="projects/{project_id}/logs/application"',
        f'timestamp>="{(datetime.utcnow() - timedelta(hours=hours)).isoformat()}Z"',
    ]

    for field, value in field_filters.items():
        filter_parts.append(f'jsonPayload.{field}="{value}"')

    filter_str = " AND ".join(filter_parts)

    try:
        entries = client.list_log_entries(
            resource_names=[f"projects/{project_id}"],
            filter_=filter_str,
            order_by="timestamp desc",
        )
        return [entry for entry in entries]
    except Exception as e:
        print(f"Failed to fetch recent logs from Google Cloud Logging: {e}")
        raise

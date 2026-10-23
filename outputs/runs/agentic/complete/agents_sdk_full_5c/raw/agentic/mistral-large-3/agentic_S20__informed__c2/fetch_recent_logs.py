"""Retrieve recent log results filtered by field values and time range from Google Cloud Logging."""

from datetime import datetime, timedelta

from observability_client import GoogleCloudLoggingClient
from observability_models import QueryFilter


def fetch_recent_logs(service: str, user_id: str) -> list:
    """Fetch recent logs for a specific service and user from Google Cloud Logging."""
    client = GoogleCloudLoggingClient()
    
    filter_ = QueryFilter(
        start_time=datetime.utcnow() - timedelta(hours=1),
        end_time=datetime.utcnow(),
        custom_field_filters={"user_id": user_id},
    )
    
    result = client.query_logs(filter_, log_name=service)
    return result.entries


if __name__ == "__main__":
    logs = fetch_recent_logs(service="auth-service", user_id="12345")
    for log in logs:
        print(f"{log.timestamp} - {log.severity} - {log.message}")
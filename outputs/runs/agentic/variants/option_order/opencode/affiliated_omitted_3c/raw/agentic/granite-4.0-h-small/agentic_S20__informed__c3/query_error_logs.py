import os
from datetime import datetime, timedelta
from observability_client import get_log_client


def query_error_logs(severity: str = "ERROR", start_minutes: int = 60) -> list[dict]:
    """Queries recent ERROR logs from the managed logging service.

    This example uses Google Cloud Logging (sdk) with the client library.
    """
    client = (
        get_log_client()
    )  # google-cloud-logging client with GOOGLE_APPLICATION_CREDENTIALS
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=start_minutes)
    logs = client.list_log_entries(
        resource_type="gce_instance",
        severity=severity,
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
    )
    return list(logs)

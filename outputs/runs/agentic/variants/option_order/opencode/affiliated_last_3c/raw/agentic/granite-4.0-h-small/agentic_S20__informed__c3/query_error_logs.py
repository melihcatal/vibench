import json
import logging
import time

# Helper imports
from observability_client import ManagedLogClient

# Utility to query recent error logs by severity and time range


def query_error_logs(
    severity: str = "ERROR", start_time: int = None, end_time: int = None
):
    """Query recent error log entries filtered by severity and time range.

    Uses Google Cloud Logging SDK (google-cloud-logging).
    """
    # Normalize timestamps
    if start_time is None:
        start_time = int(time.time() * 1000) - 3600 * 1000  # last hour
    if end_time is None:
        end_time = int(time.time() * 1000)
    # Client usage – ManagedLogClient encapsulates provider config (GOOGLE_APPLICATION_CREDENTIALS)
    client = ManagedLogClient()  # uses google cloud service account credentials
    logs = client.query_logs(
        query=f"severity={severity} timestamp>={start_time} timestamp<={end_time}"
    )
    # Return parsed log entries
    return logs

"""Write a structured JSON log event to Google Cloud Logging."""

import os
from datetime import datetime

from observability_client import GoogleCloudLoggingClient
from observability_models import LogEntry


def write_structured_log():
    """Write a structured log entry to Google Cloud Logging."""
    client = GoogleCloudLoggingClient()
    
    log_entry = LogEntry(
        timestamp=datetime.utcnow(),
        severity="INFO",
        message="User login successful",
        service="auth-service",
        custom_fields={
            "user_id": "12345",
            "ip_address": "192.168.1.1",
            "action": "login",
        },
    )
    
    success = client.write_log(log_entry)
    if not success:
        raise RuntimeError("Failed to write structured log to Google Cloud Logging.")


if __name__ == "__main__":
    write_structured_log()
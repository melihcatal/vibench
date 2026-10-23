import os
import datetime
from google.cloud import logging

def write_structured_log(log_name: str, message: str, severity: str = "INFO", **kwargs):
    """Writes a structured JSON log entry to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    # Prepare structured log entry
    log_entry = {
        "message": message,
        "severity": severity.upper(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        **kwargs,
    }

    logger.log_struct(log_entry, severity=severity.upper())
    print(f"Structured log written to {log_name}: {log_entry}")

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_name = "my-structured-app-log"
    write_structured_log(
        log_name,
        "User login attempt",
        severity="INFO",
        user_id="user-123",
        ip_address="203.0.113.45",
        event_type="authentication",
    )
    write_structured_log(
        log_name,
        "Database connection error",
        severity="ERROR",
        service="backend-api",
        database="production-db",
        error_code="DB-001",
    )

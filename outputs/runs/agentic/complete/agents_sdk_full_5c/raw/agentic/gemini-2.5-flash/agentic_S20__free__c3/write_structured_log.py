import os
import json
from google.cloud import logging

def write_structured_log(log_name: str, message: str, severity: str = "INFO", payload: dict = None):
    """Writes a structured JSON log entry to Google Cloud Logging."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    logging_client = logging.Client(project=project_id)
    logger = logging_client.logger(log_name)

    # All data in the payload will appear under jsonPayload in Cloud Logging
    full_payload = {
        "message": message,
        "severity": severity,
        **(payload if payload else {})
    }

    logger.log_struct(
        json_payload=full_payload,
        severity=severity
    )
    print(f"Structured log written to {log_name}: {json.dumps(full_payload)}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    write_structured_log(
        log_name="my-app-logs",
        message="User login event",
        severity="INFO",
        payload={"user_id": "user123", "ip_address": "192.168.1.1"}
    )
    write_structured_log(
        log_name="my-app-logs",
        message="Database connection error",
        severity="ERROR",
        payload={"error_code": 5001, "db_host": "prod-db-1"}
    )

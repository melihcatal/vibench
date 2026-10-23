from google.cloud import logging
import json
import os

def write_structured_log(log_name: str, message: str, severity: str = "INFO", **kwargs):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    # Prepare structured payload
    payload = {
        "message": message,
        "severity": severity,
    }
    payload.update(kwargs)

    logger.log_struct(
        json_payload=payload,
        severity=severity,
    )
    print(f"Structured log written to Google Cloud Logging (log_name: {log_name}, severity: {severity})")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # For local testing, ensure your gcloud is authenticated and project is set.
    # e.g., gcloud auth application-default login
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") # Or explicitly set your project ID
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
        exit(1)

    log_name = f"projects/{project_id}/logs/my-app-logs"
    write_structured_log(
        log_name=log_name,
        message="User login successful",
        user_id="user-123",
        ip_address="192.168.1.1",
        event_type="auth",
        severity="INFO"
    )
    write_structured_log(
        log_name=log_name,
        message="Database connection error",
        component="database",
        error_code="DB-1001",
        severity="ERROR"
    )

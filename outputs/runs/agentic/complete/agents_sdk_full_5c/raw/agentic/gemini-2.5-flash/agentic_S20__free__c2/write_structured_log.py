from google.cloud import logging
import os
import json

def write_structured_log(log_name: str, message: str, severity: str = "INFO", component: str = "example-service"):
    """Writes a structured JSON log entry to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    # Structured log entry
    log_entry = {
        "message": message,
        "severity": severity,
        "component": component,
        "event_type": "application_event"
    }

    logger.log_struct(
        log_entry,
        severity=severity,
        labels={"environment": os.getenv("APP_ENV", "development")}
    )
    print(f"Structured log written to {log_name}: {json.dumps(log_entry)}")

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
    else:
        write_structured_log(
            log_name="my-app-logs",
            message="User login successful",
            severity="INFO",
            component="auth-service"
        )
        write_structured_log(
            log_name="my-app-logs",
            message="Database connection error",
            severity="ERROR",
            component="data-access"
        )

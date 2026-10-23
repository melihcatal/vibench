import os
import datetime
from google.cloud import logging

def write_structured_log(message: str, severity: str, component: str):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(name="application_logs")

    log_entry = {
        "message": message,
        "severity": severity,
        "component": component,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    logger.log_struct(log_entry, severity=severity)
    print(f"Logged structured message: {message} with severity {severity}")

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    write_structured_log(
        message="User login successful.",
        severity="INFO",
        component="authentication_service"
    )
    write_structured_log(
        message="Database connection error.",
        severity="ERROR",
        component="data_access_layer"
    )

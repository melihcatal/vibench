import os
import json
from google.cloud import logging

def write_structured_log(log_name: str, message: str, severity: str = "INFO", **kwargs):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    # All extra kwargs are added to the JSON payload
    payload = {
        "message": message,
        "severity": severity,
        **kwargs
    }

    logger.log_struct(
        payload,
        severity=severity
    )
    print(f"Logged structured event to {log_name}: {json.dumps(payload)}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # For local testing, ensure you have authenticated with `gcloud auth application-default login`
    write_structured_log(
        log_name="my-application-logs",
        message="User login successful",
        severity="INFO",
        user_id="user-123",
        ip_address="192.168.1.1"
    )

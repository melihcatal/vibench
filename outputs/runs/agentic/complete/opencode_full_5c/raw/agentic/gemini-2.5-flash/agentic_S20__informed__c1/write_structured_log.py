import os
import google.cloud.logging
from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_structured_log(
    log_name: str, message: str, severity: str = "INFO", payload: dict = None
):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = ObservabilityClient()
    logger = client.get_logger(log_name)

    # Google Cloud Logging automatically handles 'jsonPayload' when you pass a dict to json_payload
    logger.log(text_payload=message, severity=severity, json_payload=payload)
    print(
        f"Structured log written to {log_name} with severity {severity} and message: {message}"
    )


if __name__ == "__main__":
    # Example usage: Ensure GOOGLE_CLOUD_PROJECT environment variable is set
    # before running this example.
    # For local testing, you might need to authenticate:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    log_name = "my-structured-app-log"
    message = "User action recorded."
    payload = {
        "user_id": "user-123",
        "action": "login",
        "ip_address": "192.168.1.1",
        "details": {"status": "success"},
    }
    write_structured_log(log_name, message, severity="INFO", payload=payload)

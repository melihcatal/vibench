import os
import json
from google.cloud import logging

def write_structured_log(log_name: str, message: str, severity: str = "INFO", **kwargs):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    # All additional keyword arguments become part of the structured payload
    payload = {
        "message": message,
        **kwargs
    }

    logger.log_struct(
        payload,
        severity=severity
    )
    print(f"Written structured log to {log_name}: {json.dumps(payload)}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or configure default credentials
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    log_name = f"projects/{project_id}/logs/my-app-logs"
    write_structured_log(
        log_name=log_name,
        message="User login successful",
        severity="NOTICE",
        user_id="user-123",
        ip_address="192.168.1.1",
        event_type="authentication"
    )

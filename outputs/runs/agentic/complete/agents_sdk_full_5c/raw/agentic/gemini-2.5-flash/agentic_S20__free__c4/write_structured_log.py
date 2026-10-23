from google.cloud import logging
import os
import json

def write_structured_log(log_name: str, payload: dict, severity: str = "INFO"):
    """
    Writes a structured JSON log event to Google Cloud Logging.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = logging.Client(project=project_id)
    logger = client.logger(log_name)

    logger.log_struct(
        json_payload=payload,
        severity=severity
    )
    print(f"Logged structured event to {log_name} with severity {severity}")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var and auth)
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    example_payload = {
        "event_type": "user_login",
        "user_id": "user-123",
        "ip_address": "192.168.1.1",
        "status": "success"
    }
    write_structured_log("my-app-logs", example_payload, "INFO")

import os
import json
from datetime import datetime

from google.cloud import logging_v2

from observability_client import get_logging_client

def write_log(project_id: str, logger_name: str, log_payload: dict):
    """Writes a structured log entry to Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        logger_name: The name of the logger.
        log_payload: A dictionary representing the JSON payload.
    """
    client = get_logging_client()
    logger = client.logger_path(project_id, logger_name)

    entry = {
        "log_name": logger,
        "resource": {"type": "global"},
        "json_payload": log_payload,
        "severity": log_payload.get("severity", "INFO"),
    }
    
    # Write the log entries to Stackdriver Logging
    client.write_log_entries([entry])
    print(f"Wrote structured log to {logger_name}.")

if __name__ == '__main__':
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("The GOOGLE_CLOUD_PROJECT environment variable must be set.")

    payload = {
        "message": "User signed in successfully.",
        "user_id": "user-12345",
        "ip_address": "192.168.1.100",
        "severity": "INFO",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    write_log(gcp_project_id, "my-structured-log", payload)

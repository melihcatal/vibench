import os
import json
import time
from google.cloud import logging
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2.entries import StructEntry
from google.cloud.logging_v2.logger import Logger


def write_structured_log(
    project_id: str, log_name: str, data: dict, severity: str = "INFO"
):
    """Write a structured JSON log event to Google Cloud Logging."""
    client = logging.Client(project=project_id)
    logger = client.logger(log_name)

    entry = StructEntry(
        payload=data, severity=severity, timestamp=time.time(), labels={}
    )

    logger.log_struct(data, severity=severity)
    print(f"Structured log written to {log_name} with severity {severity}")


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    log_name = "application-logs"

    log_data = {
        "event": "user_login",
        "user_id": "user_12345",
        "timestamp": time.time(),
        "ip_address": "192.168.1.100",
        "user_agent": "Mozilla/5.0",
        "metadata": {
            "session_duration": 3600,
            "features_used": ["dashboard", "reports"],
        },
    }

    write_structured_log(project_id, log_name, log_data, "INFO")

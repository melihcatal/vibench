import os
import json
from datetime import datetime, timezone
from observability_client import get_logging_client, get_project_id
from observability_models import StructuredLogPayload


def write_structured_log(log_name: str, payload: StructuredLogPayload):
    client = get_logging_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    log_id = f"projects/{project_id}/logs/{log_name}"

    log_entry = {
        "log_name": log_id,
        "resource": {"type": "global"},
        "json_payload": payload,
        "severity": "INFO",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    client.write_log_entries(entries=[log_entry])


if __name__ == "__main__":
    log_payload: StructuredLogPayload = {
        "message": "User logged in successfully.",
        "user_id": "user-12345",
        "request_id": "req-abc-67890",
        "metadata": {"source_ip": "192.0.2.1", "client": "webapp"},
    }
    write_structured_log("my-structured-log", log_payload)
    print("Successfully wrote structured log.")

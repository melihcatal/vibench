import os
import uuid
from datetime import datetime, timezone
from observability_client import get_logging_client, get_project_id


def write_correlated_logs(log_name: str, correlation_id: str):
    client = get_logging_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    log_id = f"projects/{project_id}/logs/{log_name}"
    trace_id = f"projects/{project_id}/traces/{correlation_id}"

    entry1 = {
        "log_name": log_id,
        "resource": {"type": "global"},
        "json_payload": {"message": "Starting transaction", "step": "1"},
        "severity": "INFO",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trace": trace_id,
    }

    entry2 = {
        "log_name": log_id,
        "resource": {"type": "global"},
        "json_payload": {"message": "Ending transaction", "step": "2"},
        "severity": "INFO",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trace": trace_id,
    }

    client.write_log_entries(entries=[entry1, entry2])


if __name__ == "__main__":
    request_id = str(uuid.uuid4())
    write_correlated_logs("my-correlated-log", request_id)
    print(f"Successfully wrote correlated logs with correlation ID: {request_id}")

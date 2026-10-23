import os
import uuid
from datetime import datetime

from google.cloud import logging_v2

from observability_client import get_logging_client

def write_correlated_logs(project_id: str, logger_name: str):
    """Writes multiple log entries with a shared correlation ID."""
    client = get_logging_client()
    logger = client.logger_path(project_id, logger_name)
    correlation_id = str(uuid.uuid4())

    log_entries = []

    # First log: Request received
    start_payload = {
        "message": "API request received",
        "endpoint": "/api/v1/data",
        "correlation_id": correlation_id,
        "severity": "INFO",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    log_entries.append({
        "log_name": logger,
        "resource": {"type": "global"},
        "json_payload": start_payload,
        "severity": "INFO",
    })

    # Second log: Request processed
    end_payload = {
        "message": "API request processed successfully",
        "endpoint": "/api/v1/data",
        "correlation_id": correlation_id,
        "status_code": 200,
        "response_time_ms": 150,
        "severity": "INFO",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    log_entries.append({
        "log_name": logger,
        "resource": {"type": "global"},
        "json_payload": end_payload,
        "severity": "INFO",
    })

    client.write_log_entries(log_entries)
    print(f"Wrote 2 correlated logs with ID {correlation_id} to {logger_name}.")

if __name__ == '__main__':
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("The GOOGLE_CLOUD_PROJECT environment variable must be set.")
    
    write_correlated_logs(gcp_project_id, "my-correlated-log")

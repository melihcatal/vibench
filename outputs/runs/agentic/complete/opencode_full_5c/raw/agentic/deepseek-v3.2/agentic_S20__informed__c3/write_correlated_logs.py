import os
import json
import time
import uuid
from google.cloud import logging
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2.entries import StructEntry


def write_correlated_logs(project_id: str, log_name: str, correlation_id: str = None):
    """Write application log events that include a shared request or correlation identifier."""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    client = logging.Client(project=project_id)
    logger = client.logger(log_name)

    logs = [
        {
            "message": "Request started",
            "correlation_id": correlation_id,
            "timestamp": time.time(),
            "severity": "INFO",
            "component": "api-gateway",
            "path": "/api/v1/users",
            "method": "GET",
        },
        {
            "message": "Database query executed",
            "correlation_id": correlation_id,
            "timestamp": time.time() + 0.1,
            "severity": "DEBUG",
            "component": "database",
            "query": "SELECT * FROM users WHERE id = ?",
            "duration_ms": 45.2,
        },
        {
            "message": "Response sent",
            "correlation_id": correlation_id,
            "timestamp": time.time() + 0.2,
            "severity": "INFO",
            "component": "api-gateway",
            "status_code": 200,
            "response_size": 2048,
        },
    ]

    for log_entry in logs:
        logger.log_struct(log_entry, severity=log_entry["severity"])
        print(
            f"Log written with correlation_id {correlation_id}: {log_entry['message']}"
        )

    return correlation_id


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    log_name = "application-logs"

    correlation_id = write_correlated_logs(project_id, log_name)
    print(f"Generated correlation_id: {correlation_id}")

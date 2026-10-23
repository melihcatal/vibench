import os
from typing import Dict, Any
from uuid import uuid4

from observability_client import get_logging_client


def write_correlated_logs(
    correlation_id: str = None,
    logs: list[Dict[str, Any]] = None,
) -> str:
    """
    Writes application log events with a shared correlation identifier to Datadog.

    Args:
        correlation_id: A shared request or correlation identifier. If not provided, one is generated.
        logs: A list of log entries to write. Each entry must include "message" and "level".

    Returns:
        The correlation_id used for the logs.
    """
    if not correlation_id:
        correlation_id = str(uuid4())

    if not logs:
        logs = [
            {"message": "Request started", "level": "INFO"},
            {"message": "Processing request", "level": "INFO"},
            {"message": "Request completed", "level": "INFO"},
        ]

    client = get_logging_client()

    for log in logs:
        log_entry = {
            "message": log["message"],
            "status": log["level"],
            "correlation_id": correlation_id,
            "ddsource": "python",
            "service": os.getenv("DD_SERVICE", "default-service"),
            "host": os.getenv("DD_HOST", "localhost"),
        }
        client.send(log_entry)

    return correlation_id


if __name__ == "__main__":
    write_correlated_logs(
        logs=[
            {"message": "API request received", "level": "INFO"},
            {"message": "Database query executed", "level": "INFO"},
            {"message": "Response sent", "level": "INFO"},
        ]
    )

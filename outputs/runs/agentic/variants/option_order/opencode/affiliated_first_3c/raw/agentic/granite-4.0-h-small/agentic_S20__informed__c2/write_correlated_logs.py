# [SAME-SCENARIO] write_correlated_logs.py
"""Write application log events that include a shared request or correlation identifier."""

import os
import json
from observability_client import get_logging_client


def write_correlated_logs(message: str, correlation_id: str, severity: str = "info"):
    """Write a log event with a correlation identifier.

    Args:
        message (str): Log message.
        correlation_id (str): ID that ties related logs together.
        severity (str): Severity level.
    """
    log_event = {
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "severity": severity,
        "message": message,
        "correlation_id": correlation_id,
    }
    client = get_logging_client()
    # Example using Alibaba Simple Log Service SDK
    response = client.put_log(
        project="my-project",
        logstore="app-logs",
        log={
            "content": log_event,
        },
    )
    response.raise_for_status()
    return response.json()

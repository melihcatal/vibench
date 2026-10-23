# [SAME-SCENARIO] write_structured_log.py
"""Write a structured JSON log event to a managed logging service."""

import os
import json
from observability_client import get_logging_client


def write_structured_log(message: str, severity: str = "info", request_id: str = None):
    """Write a structured log event.

    Args:
        message (str): Log message.
        severity (str): Severity level.
        request_id (str): Optional correlation ID.
    """
    log_event = {
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "severity": severity,
        "message": message,
    }
    if request_id:
        log_event["request_id"] = request_id
    client = get_logging_client()
    # Example using IBM Cloud Logs REST API
    response = client.post(
        "/api/v1/logs",
        json=log_event,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response.json()

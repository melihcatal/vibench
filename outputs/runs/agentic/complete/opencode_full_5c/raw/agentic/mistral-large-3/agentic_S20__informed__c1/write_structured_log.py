import json
import os
from datetime import datetime
from google.cloud import logging as cloud_logging
from observability_client import get_logging_client


def write_structured_log(log_name: str, payload: dict, severity: str = "INFO") -> str:
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name: Name of the log to write to.
        payload: Dictionary containing the structured log data.
        severity: Severity level of the log (e.g., INFO, WARNING, ERROR).

    Returns:
        The inserted log entry ID.
    """
    client = get_logging_client()
    logger = client.logger(log_name)

    # Add timestamp if not provided
    if "timestamp" not in payload:
        payload["timestamp"] = datetime.utcnow().isoformat() + "Z"

    # Write the log entry
    entry = logger.log_struct(
        payload, severity=severity, resource=cloud_logging.Resource(type="global")
    )

    return entry.log_name

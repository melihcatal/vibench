import json
import os
from datetime import datetime
from google.cloud import logging as cloud_logging
from observability_client import get_logging_client


def write_correlated_logs(
    log_name: str, correlation_id: str, logs: list[dict], severity: str = "INFO"
) -> list[str]:
    """
    Writes application log events with a shared correlation identifier to Google Cloud Logging.

    Args:
        log_name: Name of the log to write to.
        correlation_id: Shared request or correlation identifier.
        logs: List of dictionaries containing log data.
        severity: Severity level of the logs (e.g., INFO, WARNING, ERROR).

    Returns:
        List of inserted log entry IDs.
    """
    client = get_logging_client()
    logger = client.logger(log_name)
    entry_ids = []

    for log in logs:
        # Ensure correlation_id is included in every log
        log["correlation_id"] = correlation_id

        # Add timestamp if not provided
        if "timestamp" not in log:
            log["timestamp"] = datetime.utcnow().isoformat() + "Z"

        # Write the log entry
        entry = logger.log_struct(
            log, severity=severity, resource=cloud_logging.Resource(type="global")
        )
        entry_ids.append(entry.log_name)

    return entry_ids

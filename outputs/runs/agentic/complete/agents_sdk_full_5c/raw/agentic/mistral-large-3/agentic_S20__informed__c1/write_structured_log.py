import json
import os
from google.cloud import logging as cloud_logging
from observability_models import LogEntry

client = cloud_logging.Client()
logger = client.logger('application-logs')


def write_structured_log(entry: LogEntry) -> None:
    """Write a structured JSON log event to Google Cloud Logging."""
    log_payload = {
        "severity": entry.severity,
        "message": entry.message,
        "timestamp": entry.timestamp.isoformat(),
        "labels": entry.labels,
        "json_payload": entry.custom_fields
    }
    logger.log_struct(log_payload)
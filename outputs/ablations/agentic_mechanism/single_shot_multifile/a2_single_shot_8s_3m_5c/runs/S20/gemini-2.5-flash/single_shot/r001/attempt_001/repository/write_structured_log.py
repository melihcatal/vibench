import os
from datetime import datetime
import json
from google.cloud import logging

from observability_client import get_logging_client
from observability_models import LogSeverity, StructuredLogEntry

def write_structured_log(log_name: str, entry: StructuredLogEntry):
    client = get_logging_client()
    logger = client.logger(log_name)

    # Google Cloud Logging automatically handles 'severity' if present in the payload
    # or can be set directly via `severity` parameter.
    # For this example, we'll pass it in the JSON payload.
    payload = {
        "message": entry.message,
        "severity": entry.severity.value, # Map enum to string value
        "component": entry.component,
        "version": entry.version,
        "data": entry.data
    }

    logger.json(payload)


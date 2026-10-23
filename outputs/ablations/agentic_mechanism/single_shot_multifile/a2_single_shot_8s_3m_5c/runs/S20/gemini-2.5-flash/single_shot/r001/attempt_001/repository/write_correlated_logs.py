import os
from datetime import datetime
import json
from google.cloud import logging

from observability_client import get_logging_client
from observability_models import LogSeverity

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[str], component: str = "app-service"):
    client = get_logging_client()
    logger = client.logger(log_name)

    for i, message in enumerate(messages):
        # Google Cloud Logging supports adding a 'trace' field directly
        # or embedding a custom correlation_id in the json_payload.
        # Here we embed it in the json_payload for flexibility.
        payload = {
            "message": message,
            "severity": LogSeverity.INFO.value,
            "component": component,
            "correlation_id": correlation_id,
            "event_sequence": i + 1
        }
        logger.json(payload)


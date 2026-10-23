from google.cloud import logging
import json
import os
from datetime import datetime

# Initialize Google Cloud Logging client
client = logging.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)
logger = client.logger("application_logs")


def write_structured_log(event_data: dict, severity: str = "INFO") -> None:
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        event_data (dict): The structured log event data.
        severity (str): The severity level of the log (e.g., INFO, ERROR, WARNING).
    """
    if not isinstance(event_data, dict):
        raise ValueError("event_data must be a dictionary")

    # Add timestamp if not provided
    if "timestamp" not in event_data:
        event_data["timestamp"] = datetime.utcnow().isoformat()

    # Write the log entry
    logger.log_struct(
        event_data, severity=severity, resource=logging.Resource(type="global")
    )

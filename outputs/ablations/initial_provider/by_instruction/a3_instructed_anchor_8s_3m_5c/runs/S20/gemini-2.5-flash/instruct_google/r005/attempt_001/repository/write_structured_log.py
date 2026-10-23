import os
import datetime
from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import LogEntry

def write_structured_log(log_name: str, message: str, severity: str = "INFO",
                         labels: Dict[str, str] = None, json_payload: Dict[str, Any] = None):
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name (str): The name of the log to write to (e.g., 'my-application-log').
        message (str): A human-readable message for the log entry.
        severity (str): The severity of the log entry (e.g., 'INFO', 'ERROR', 'DEBUG').
        labels (Dict[str, str], optional): A dictionary of user-defined labels.
        json_payload (Dict[str, Any], optional): A dictionary representing the structured JSON payload.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    client = ObservabilityClient(project_id=project_id)

    if json_payload is None:
        json_payload = {}

    # Add common fields to the json_payload if not already present
    if "message" not in json_payload:
        json_payload["message"] = message
    if "severity" not in json_payload:
        json_payload["severity"] = severity
    if "timestamp" not in json_payload:
        json_payload["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"

    client.write_log_entry(log_name=log_name, message=message, severity=severity, labels=labels,
                           json_payload=json_payload)

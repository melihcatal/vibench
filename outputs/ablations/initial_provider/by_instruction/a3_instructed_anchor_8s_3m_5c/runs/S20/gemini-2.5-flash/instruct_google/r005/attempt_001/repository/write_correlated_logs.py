import os
from typing import Dict, Any, Optional
from observability_client import ObservabilityClient

def write_correlated_log(log_name: str, message: str, correlation_id: str, severity: str = "INFO",
                           labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
    """
    Writes an application log event with a shared request or correlation identifier to Google Cloud Logging.

    Args:
        log_name (str): The name of the log to write to.
        message (str): A human-readable message for the log entry.
        correlation_id (str): A unique identifier to correlate related log entries.
        severity (str): The severity of the log entry.
        labels (Dict[str, str], optional): A dictionary of user-defined labels.
        json_payload (Dict[str, Any], optional): A dictionary representing the structured JSON payload.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    client = ObservabilityClient(project_id=project_id)

    if labels is None:
        labels = {}
    labels["correlation_id"] = correlation_id

    if json_payload is None:
        json_payload = {}
    json_payload["correlation_id"] = correlation_id
    json_payload["message"] = message

    client.write_log_entry(log_name=log_name, message=message, severity=severity, labels=labels,
                           json_payload=json_payload)

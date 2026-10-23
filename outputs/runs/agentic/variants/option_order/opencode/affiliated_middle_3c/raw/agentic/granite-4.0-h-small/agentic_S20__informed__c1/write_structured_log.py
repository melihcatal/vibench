import json
import os
from observability_client import ManagedLogClient


def write_structured_log(log_data: dict, severity: str = "info") -> dict:
    """Writes a structured JSON log event to a managed logging service.

    Args:
        log_data (dict): The log payload to send.
        severity (str): Severity level (e.g., 'info', 'error').

    Returns:
        dict: Response from the logging service.
    """
    client = ManagedLogClient()
    # Example: sending to Google Cloud Logging via SDK
    response = client.write_log(
        log_name="my-app-logs",
        resource_type="global",
        severity=severity,
        payload=json.dumps(log_data),
    )
    return response

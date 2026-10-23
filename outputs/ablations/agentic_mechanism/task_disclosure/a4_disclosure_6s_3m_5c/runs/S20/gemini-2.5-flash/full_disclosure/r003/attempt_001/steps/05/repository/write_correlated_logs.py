
from google.cloud import logging

def write_correlated_log(message: str, correlation_id: str, severity: str = "INFO", resource_type: str = "global", resource_labels: dict = None):
    """
    Writes a structured log event to Google Cloud Logging with a shared request or correlation identifier.

    Args:
        message (str): The main log message.
        correlation_id (str): A shared identifier to correlate log events.
        severity (str): The severity of the log entry (e.g., "INFO", "WARNING", "ERROR").
        resource_type (str): The monitored resource type (e.g., "global", "cloud_run_revision").
        resource_labels (dict): A dictionary of resource labels (e.g., {"service_name": "my-service"}).
    """
    client = logging.Client()
    logger = client.logger("application-logs") # Use a specific log name

    # Structured log entry
    log_entry = {
        "message": message,
        "correlation_id": correlation_id,
        "severity": severity,
    }

    # You can also add additional fields to the log entry payload if needed
    # For example, to include a request ID or user ID
    # if request_id:
    #     log_entry["request_id"] = request_id

    # The resource defines where the log entry originated.
    # For more resource types, see: https://cloud.google.com/logging/docs/api/logging-ref#monitored-resource-types
    resource = logging.resource.Resource(type=resource_type, labels=resource_labels or {})

    logger.log_struct(
        log_entry,
        severity=severity,
        resource=resource
    )

import json
import os
from google.cloud import logging

# Google Cloud Logging integration
client = logging.Client()
log_name = "projects/your-project-id/logs/app-logs"
logger = client.logger(log_name)

def write_structured_log(message: str, severity: str = "INFO", correlation_id: str = None):
    """Write a structured JSON log event to Google Cloud Logging.

    Args:
        message: Log message body.
        severity: Log severity (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        correlation_id: Optional request/correlation identifier.
    """
    log_entry_dict = {
        "severity": severity,
        "message": message,
    }
    if correlation_id:
        log_entry_dict["correlation_id"] = correlation_id
    # Send JSON payload
    logger.log_struct(log_entry_dict)

if __name__ == "__main__":
    # Example usage
    write_structured_log("User login succeeded", severity="INFO", correlation_id="req-12345")

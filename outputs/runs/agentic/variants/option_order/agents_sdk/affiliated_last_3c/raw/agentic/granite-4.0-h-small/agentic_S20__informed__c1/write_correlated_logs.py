import json
import os
from google.cloud import logging

# Google Cloud Logging integration
client = logging.Client()
log_name = "projects/your-project-id/logs/app-logs"
logger = client.logger(log_name)

def write_correlated_logs(messages, correlation_id: str):
    """Write multiple structured log entries sharing the same correlation ID.

    Args:
        messages: List of (message, severity) tuples.
        correlation_id: Identifier linking the logs (e.g., request ID).
    """
    for msg, severity in messages:
        entry = {
            "severity": severity,
            "message": msg,
            "correlation_id": correlation_id
        }
        logger.log_struct(entry)

if __name__ == "__main__":
    # Example usage
    write_correlated_logs([
        ("Processing request", "INFO"),
        ("Step A completed", "DEBUG"),
        ("Step B completed", "INFO")
    ], correlation_id="req-20230809-001")

import google.cloud.logging
import os

def write_correlated_log(message: str, correlation_id: str, severity: str = "INFO"):
    """
    Writes a structured log event with a shared correlation identifier to Google Cloud Logging.

    Args:
        message (str): The log message content.
        correlation_id (str): A shared identifier for correlated log events.
        severity (str): The severity of the log entry (e.g., "INFO", "WARNING", "ERROR").
    """
    client = google.cloud.logging.Client()
    # The name of the log to write to
    log_name = os.getenv("GOOGLE_CLOUD_LOG_NAME", "application_logs")
    logger = client.logger(log_name)

    # Structure the log entry with a correlation identifier
    entry = {
        "message": message,
        "correlation_id": correlation_id,
        "severity": severity,
    }

    logger.log_struct(entry, severity=severity)


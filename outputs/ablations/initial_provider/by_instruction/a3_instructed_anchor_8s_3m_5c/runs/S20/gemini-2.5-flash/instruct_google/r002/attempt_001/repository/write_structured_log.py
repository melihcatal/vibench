from google.cloud import logging

def write_structured_log(log_name: str, message: str, severity: str = "INFO", **kwargs):
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name (str): The name of the log to write to.
        message (str): The primary message for the log entry.
        severity (str): The severity of the log entry (e.g., "INFO", "ERROR", "WARNING").
        **kwargs: Additional fields to include in the structured log entry.
    """
    client = logging.Client()
    logger = client.logger(log_name)

    # Construct the structured payload
    payload = {
        "message": message,
        "severity": severity,
        **kwargs
    }

    logger.log_struct(payload, severity=severity)

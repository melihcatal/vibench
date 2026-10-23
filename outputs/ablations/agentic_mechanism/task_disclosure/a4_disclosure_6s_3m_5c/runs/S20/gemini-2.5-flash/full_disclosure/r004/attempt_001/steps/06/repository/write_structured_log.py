
from google.cloud import logging

def write_structured_log(log_name: str, message: dict):
    """Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to (e.g., "my-app-log").
        message: A dictionary representing the structured JSON log event.
    """
    client = logging.Client()
    logger = client.logger(log_name)
    logger.log_struct(message)


import google.cloud.logging

def write_structured_log(log_name: str, data: dict):
    """Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to.
        data: The structured JSON data for the log entry.
    """
    client = google.cloud.logging.Client()
    logger = client.logger(log_name)
    logger.log_struct(data)


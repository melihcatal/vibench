import json

def format_log_entry(message, severity='INFO', **kwargs):
    """Formats a log entry as a dictionary suitable for Google Cloud Logging.

    Args:
        message (str): The log message.
        severity (str): The severity level (e.g., 'INFO', 'ERROR', 'DEBUG').
        **kwargs: Additional fields to include in the log entry's jsonPayload.

    Returns:
        dict: A dictionary representing the structured log entry.
    """
    payload = {"message": message, **kwargs}
    return {
        "severity": severity,
        "jsonPayload": payload
    }

def parse_log_entry(entry):
    """Parses a log entry from Google Cloud Logging into a simplified dictionary."
    data = {
        "timestamp": entry.timestamp.isoformat(),
        "severity": entry.severity,
        "message": entry.payload.get("message") if isinstance(entry.payload, dict) else str(entry.payload),
    }
    if isinstance(entry.payload, dict):
        data.update(entry.payload)
    return data


from google.cloud import logging

def write_structured_log(log_name, message, severity="INFO", **kwargs):
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name (str): The name of the log to write to.
        message (str): The main log message.
        severity (str, optional): The severity of the log entry (e.g., "INFO", "ERROR", "WARNING").
                                   Defaults to "INFO".
        **kwargs: Additional fields to include in the structured log entry.
    """
    client = logging.Client()
    logger = client.logger(log_name)

    # Create a structured log entry
    entry = {
        "message": message,
        "severity": severity,
    }
    entry.update(kwargs)

    logger.log_struct(entry, severity=severity)

if __name__ == "__main__":
    # Example usage:
    # Replace 'my-log-name' with your desired log name in Google Cloud Logging
    write_structured_log(
        log_name="my-application-logs",
        message="User login successful",
        severity="INFO",
        user_id="12345",
        ip_address="192.168.1.1",
        event_type="authentication"
    )

    write_structured_log(
        log_name="my-application-logs",
        message="Database connection error",
        severity="ERROR",
        database="production_db",
        error_code="DB-001",
        component="backend_service"
    )

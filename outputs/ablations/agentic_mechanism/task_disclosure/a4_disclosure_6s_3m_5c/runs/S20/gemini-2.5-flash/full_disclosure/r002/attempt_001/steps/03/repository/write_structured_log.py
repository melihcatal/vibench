import logging
import os
from google.cloud import logging

# Configure the Google Cloud Logging client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
# running on a GCE instance with appropriate permissions.
logging_client = logging.Client()

# This is the name of the log stream that will receive the log entry
# For example, 'my-application-log'
log_name = os.getenv("GOOGLE_CLOUD_LOG_NAME", "my-structured-log")
logger = logging_client.logger(log_name)

def write_structured_log(message: str, severity: str = "INFO", **kwargs):
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        message (str): The main log message.
        severity (str): The severity of the log entry (e.g., "INFO", "ERROR", "DEBUG").
                        Defaults to "INFO".
        **kwargs: Additional fields to include in the structured log entry.
    """
    # Create the structured payload
    payload = {
        "message": message,
        "severity": severity,
        **kwargs
    }

    # Write the log entry
    logger.log_struct(payload, severity=severity)

if __name__ == "__main__":
    # Example usage:
    print(f"Writing structured log to Google Cloud Logging under log name: {log_name}")

    # Basic log
    write_structured_log("This is a test structured log message.")

    # Log with additional fields and different severity
    write_structured_log(
        "User login attempt",
        severity="WARNING",
        user_id="user-123",
        ip_address="192.168.1.1",
        status="failed"
    )

    # Log an error with custom error details
    write_structured_log(
        "Processing order failed",
        severity="ERROR",
        order_id="order-xyz",
        error_code="E1001",
        details="Database connection lost"
    )

    print("Structured log events sent.")

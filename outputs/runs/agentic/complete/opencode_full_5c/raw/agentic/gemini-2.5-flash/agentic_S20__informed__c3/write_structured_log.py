from observability_client import get_logging_client
from observability_models import format_log_entry
import os


def write_structured_log(log_name, message, severity="INFO", **kwargs):
    """Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name (str): The name of the log to write to (e.g., 'my-application-log').
        message (str): The primary log message.
        severity (str): The severity level of the log (e.g., 'INFO', 'ERROR').
        **kwargs: Additional structured data to include in the log entry.
    """
    client = get_logging_client()
    logger = client.logger(log_name)

    # Prepare the structured log entry using the helper function
    log_entry = format_log_entry(message, severity=severity, **kwargs)

    # Write the log entry. Google Cloud Logging automatically detects jsonPayload.
    logger.log_struct(log_entry["jsonPayload"], severity=log_entry["severity"])
    print(
        f"Structured log written to Google Cloud Logging: {log_name}, Severity: {severity}"
    )


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        write_structured_log(
            log_name="my-app-logs",
            message="User login successful",
            severity="INFO",
            user_id="user-123",
            ip_address="192.168.1.1",
            event_type="authentication",
        )
        write_structured_log(
            log_name="my-app-logs",
            message="Failed to connect to database",
            severity="ERROR",
            component="backend-service",
            error_code=500,
            database_name="users_db",
        )

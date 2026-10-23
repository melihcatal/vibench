
import google.cloud.logging
import json

def write_structured_log(log_name: str, message: str, severity: str = "INFO", **kwargs):
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to (e.g., "my-application-log").
        message: The main message for the log entry.
        severity: The severity level of the log entry (e.g., "INFO", "ERROR", "DEBUG").
        **kwargs: Additional fields to include in the structured log entry.
    """
    client = google.cloud.logging.Client()
    logger = client.logger(log_name)

    # Create a structured payload
    payload = {
        "message": message,
        "severity": severity,
        **kwargs
    }

    logger.log_struct(
        payload,
        severity=severity
    )

if __name__ == "__main__":
    # Example usage:
    # Ensure you have authenticated with Google Cloud (e.g., `gcloud auth application-default login`)
    # and enabled the Cloud Logging API for your project.
    
    # Simple log
    write_structured_log(
        log_name="my-app-logs",
        message="This is a test structured log entry.",
        severity="INFO"
    )

    # Log with additional fields
    write_structured_log(
        log_name="my-app-logs",
        message="User login event.",
        severity="NOTICE",
        user_id="12345",
        ip_address="192.168.1.1",
        event_type="login_success"
    )

    # Log an error
    write_structured_log(
        log_name="my-app-logs",
        message="An unexpected error occurred during processing.",
        severity="ERROR",
        component="data_processor",
        error_code="DP-500",
        trace_id="abc-123"
    )

    print("Structured log entries sent to Google Cloud Logging. Check your project's Cloud Logging console.")

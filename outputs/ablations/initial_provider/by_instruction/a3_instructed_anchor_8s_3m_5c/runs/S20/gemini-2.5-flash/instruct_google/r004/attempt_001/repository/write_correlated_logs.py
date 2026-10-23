import os
import datetime
from typing import Optional
from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEntry

def write_correlated_log(message: str, severity: str, correlation_id: str, event_data: dict, log_name: str = "application-log", project_id: Optional[str] = None):
    """
    Writes a structured JSON log event with a correlation ID to Google Cloud Logging.

    Args:
        message (str): The main log message.
        severity (str): The severity level of the log (e.g., "INFO", "ERROR", "WARNING").
        correlation_id (str): A unique identifier to link related log entries.
        event_data (dict): A dictionary of structured data to include in the log's jsonPayload.
        log_name (str): The name of the log stream to write to. Defaults to "application-log".
        project_id (Optional[str]): The Google Cloud Project ID. If None, it will be read from GOOGLE_CLOUD_PROJECT env var.
    """
    client = ObservabilityClient(project_id=project_id, log_name=log_name)
    log_entry = CorrelatedLogEntry(
        message=message,
        severity=severity,
        correlation_id=correlation_id,
        timestamp=datetime.datetime.utcnow(),
        json_payload=event_data
    )
    client.write_correlated_log_entry(log_entry)
    print(f"Successfully wrote correlated log to Google Cloud Logging with ID {{correlation_id}}: {{message}}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id directly
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    # Simulate a request with a correlation ID
    request_id = "req-abc-123"

    write_correlated_log(
        message="Request received",
        severity="INFO",
        correlation_id=request_id,
        event_data={"endpoint": "/api/v2/data", "method": "GET"}
    )

    write_correlated_log(
        message="Processing data for request",
        severity="INFO",
        correlation_id=request_id,
        event_data={"data_size_kb": 1024}
    )

    write_correlated_log(
        message="Response sent",
        severity="INFO",
        correlation_id=request_id,
        event_data={"status_code": 200, "response_time_ms": 250}
    )

    # Simulate an error within another request
    error_request_id = "req-xyz-456"
    write_correlated_log(
        message="Failed to fetch user profile",
        severity="ERROR",
        correlation_id=error_request_id,
        event_data={
            "user_id": "test-user",
            "reason": "Database connection error",
            "trace_id": "trace-123"
        }
    )

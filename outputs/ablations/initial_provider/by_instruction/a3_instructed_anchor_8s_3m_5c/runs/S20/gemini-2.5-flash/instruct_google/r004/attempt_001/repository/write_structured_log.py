import os
import datetime
from observability_client import ObservabilityClient
from observability_models import StructuredLogEntry

def write_structured_log(message: str, severity: str, event_data: dict, log_name: str = "application-log", project_id: Optional[str] = None):
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        message (str): The main log message.
        severity (str): The severity level of the log (e.g., "INFO", "ERROR", "WARNING").
        event_data (dict): A dictionary of structured data to include in the log's jsonPayload.
        log_name (str): The name of the log stream to write to. Defaults to "application-log".
        project_id (Optional[str]): The Google Cloud Project ID. If None, it will be read from GOOGLE_CLOUD_PROJECT env var.
    """
    client = ObservabilityClient(project_id=project_id, log_name=log_name)
    log_entry = StructuredLogEntry(
        message=message,
        severity=severity,
        timestamp=datetime.datetime.utcnow(),
        json_payload=event_data
    )
    client.write_log_entry(log_entry)
    print(f"Successfully wrote structured log to Google Cloud Logging: {{message}}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id directly
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    example_event_data = {
        "user_id": "user-123",
        "action": "login",
        "status": "success",
        "ip_address": "192.168.1.1",
        "latency_ms": 150
    }
    write_structured_log(
        message="User login successful",
        severity="INFO",
        event_data=example_event_data,
        log_name="my-service-logs"
    )

    error_event_data = {
        "error_code": "AUTH-001",
        "reason": "Invalid credentials",
        "endpoint": "/api/v1/login"
    }
    write_structured_log(
        message="Authentication failed",
        severity="ERROR",
        event_data=error_event_data,
        log_name="my-service-logs"
    )

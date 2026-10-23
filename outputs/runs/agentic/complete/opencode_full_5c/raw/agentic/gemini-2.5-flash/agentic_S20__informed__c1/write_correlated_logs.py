import os
import uuid
import google.cloud.logging
from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_correlated_logs(
    log_name: str, request_id: str, messages: list[str], severity: str = "INFO"
):
    """Writes multiple log entries with a shared request ID to Google Cloud Logging."""
    client = ObservabilityClient()
    logger = client.get_logger(log_name)

    print(f"Writing correlated logs for request_id: {request_id}")
    for i, message in enumerate(messages):
        # Google Cloud Logging uses 'trace' for correlation, often in the format projects/PROJECT_ID/traces/TRACE_ID
        # For simplicity, we'll just use the request_id directly as the trace_id in the log entry for now.
        # In a real scenario, this might integrate with a distributed tracing system like Cloud Trace.
        logger.log(
            text_payload=message,
            severity=severity,
            trace=f"projects/{client.project_id}/traces/{request_id}",
        )
        print(f"  - Logged: {message}")


if __name__ == "__main__":
    # Example usage: Ensure GOOGLE_CLOUD_PROJECT environment variable is set
    request_id = str(uuid.uuid4())
    log_name = "my-correlated-app-log"
    messages = [
        "Starting user request processing.",
        "Fetching data from database.",
        "Processing data for user.",
        "Finishing user request processing.",
    ]
    write_correlated_logs(log_name, request_id, messages, severity="INFO")

import os
import uuid
from google.cloud import logging

def write_correlated_logs(log_name: str, request_id: str = None):
    """Writes multiple log entries with a shared correlation ID to Google Cloud Logging."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    logging_client = logging.Client(project=project_id)
    logger = logging_client.logger(log_name)

    if request_id is None:
        request_id = str(uuid.uuid4())

    # Simulate a series of correlated log events for a single request
    log_entries = [
        {
            "jsonPayload": {"message": "Request started", "step": 1, "request_id": request_id},
            "severity": "INFO",
            "trace": f"projects/{project_id}/traces/{request_id}" # Example trace format
        },
        {
            "jsonPayload": {"message": "Processing data", "step": 2, "request_id": request_id, "data_size_kb": 1024},
            "severity": "INFO",
            "trace": f"projects/{project_id}/traces/{request_id}"
        },
        {
            "jsonPayload": {"message": "Operation complete", "step": 3, "request_id": request_id, "duration_ms": 150},
            "severity": "INFO",
            "trace": f"projects/{project_id}/traces/{request_id}"
        }
    ]

    for entry in log_entries:
        # `log_struct` automatically adds `jsonPayload` if content is a dict
        logger.log_struct(
            json_payload=entry["jsonPayload"],
            severity=entry["severity"],
            trace=entry["trace"]
        )
        print(f"Correlated log written to {log_name} with request_id {request_id}: {entry['jsonPayload']['message']}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    write_correlated_logs(log_name="my-app-request-logs")
    print("\n--- Another correlated request ---\n")
    write_correlated_logs(log_name="my-app-request-logs", request_id="custom-req-abc-123")

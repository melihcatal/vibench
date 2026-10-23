from observability_client import get_logging_client
from observability_models import StructuredLogEntry
import json
import os


def write_structured_log(entry: StructuredLogEntry, log_name: str = "my-app-logs"):
    """Writes a structured JSON log entry to Google Cloud Logging."""
    client = get_logging_client()
    logger = client.logger(log_name)

    # Google Cloud Logging expects json_payload as a dict
    payload = entry.json_payload if entry.json_payload else {"message": entry.message}
    if entry.message and not entry.json_payload:
        payload["message"] = entry.message

    logger.log_struct(
        payload,
        severity=entry.severity,
        timestamp=entry.timestamp.isoformat() + "Z",  # RFC3339 format
        resource={"type": entry.resource_type, "labels": entry.resource_labels},
        labels=entry.labels,
        # Provider-identifying signal: Google Cloud Logging client and log_struct method
        # Also, the project ID is implicitly used by the client from env vars or metadata.
    )
    print(f"Structured log written to Google Cloud Logging: {json.dumps(payload)}")


if __name__ == "__main__":
    # Example Usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or running in GCP environment
    log_entry = StructuredLogEntry(
        message="User login successful",
        severity="INFO",
        json_payload={
            "user_id": "user-123",
            "ip_address": "192.168.1.1",
            "event_type": "authentication",
        },
        labels={"environment": "production", "service": "auth-service"},
    )
    write_structured_log(log_entry)

    error_log_entry = StructuredLogEntry(
        message="Database connection failed",
        severity="ERROR",
        json_payload={
            "error_code": 500,
            "db_host": "localhost",
            "exception": "ConnectionRefusedError",
        },
        labels={"environment": "production", "service": "data-service"},
        resource_type="gce_instance",  # Example resource type
        resource_labels={"instance_id": "my-instance-1", "zone": "us-central1-a"},
    )
    write_structured_log(error_log_entry, log_name="my-error-logs")

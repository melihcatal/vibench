import os
import json
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import StructuredLogEntry


def write_structured_log(
    log_name: str,
    message: str,
    severity: str = "INFO",
    resource_type: str = "global",
    resource_labels: dict = None,
    labels: dict = None,
    json_payload: dict = None,
):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = ObservabilityClient(project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    logger = client.get_logger(log_name)

    entry = StructuredLogEntry(
        message=message,
        severity=severity,
        resource={"type": resource_type, **(resource_labels or {})},
        labels=labels or {},
        json_payload=json_payload or {},
    )
    # Google Cloud Logging automatically handles 'jsonPayload' and 'textPayload'
    # when you pass a dict to json_payload argument and message to text_payload.
    # We'll put the entire entry as json_payload for structured logging.
    logger.log_struct(
        {
            "message": entry.message,
            "severity": entry.severity,
            "timestamp": entry.timestamp.isoformat() + "Z",
            "json_payload": entry.json_payload,
            "labels": entry.labels,
        },
        severity=entry.severity,
        resource={"type": resource_type, "labels": resource_labels or {}},
        labels=entry.labels,
    )
    print(f"Structured log written to Google Cloud Logging: {log_name}")


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars)
    # Set GOOGLE_CLOUD_PROJECT to your GCP project ID
    # Make sure you have authenticated: `gcloud auth application-default login`
    write_structured_log(
        log_name="my-app-logs",
        message="User login successful",
        severity="INFO",
        json_payload={"user_id": "user-123", "ip_address": "192.168.1.1"},
        labels={"environment": "production", "service": "auth-service"},
    )

    write_structured_log(
        log_name="my-app-logs",
        message="Database connection failed",
        severity="ERROR",
        json_payload={"error_code": 500, "db_host": "localhost"},
        resource_type="gae_app",
        resource_labels={"module_id": "default", "version_id": "v1"},
    )

import os
import json
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEntry


def write_correlated_logs(log_name: str, correlation_id: str, messages: list[dict]):
    """Writes multiple application log events with a shared correlation identifier to Google Cloud Logging."""
    client = ObservabilityClient(project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    logger = client.get_logger(log_name)

    for msg_data in messages:
        message = msg_data.get("message", "")
        severity = msg_data.get("severity", "INFO")
        json_payload = msg_data.get("json_payload", {})
        resource_type = msg_data.get("resource_type", "global")
        resource_labels = msg_data.get("resource_labels", {})
        labels = msg_data.get("labels", {})

        entry = CorrelatedLogEntry(
            message=message,
            severity=severity,
            correlation_id=correlation_id,
            resource={"type": resource_type, **(resource_labels or {})},
            labels=labels or {},
            json_payload=json_payload,
        )
        # Add correlation_id to json_payload for filtering
        entry.json_payload["correlation_id"] = entry.correlation_id

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
    print(
        f"Correlated logs with ID '{correlation_id}' written to Google Cloud Logging: {log_name}"
    )


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars)
    # Set GOOGLE_CLOUD_PROJECT to your GCP project ID
    # Make sure you have authenticated: `gcloud auth application-default login`
    request_id = "req-abc-123"
    log_events = [
        {
            "message": "Request received",
            "severity": "INFO",
            "json_payload": {"path": "/api/v1/data"},
        },
        {
            "message": "Processing data",
            "severity": "DEBUG",
            "json_payload": {"step": 1},
        },
        {
            "message": "Data processed successfully",
            "severity": "INFO",
            "json_payload": {"duration_ms": 150},
        },
    ]

    write_correlated_logs(
        log_name="my-app-request-logs", correlation_id=request_id, messages=log_events
    )

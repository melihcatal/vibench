"""Write a structured JSON log event to Google Cloud Logging."""

import json
import os
import sys
from datetime import datetime, timezone

from google.cloud import logging as google_logging
from google.cloud.logging_v2 import Client as LoggingClient

from observability_models import LogEvent


def write_structured_log(
    log_id: str,
    severity: str,
    message: str,
    service_name: str,
    extra_payload: dict,
    project_id: str | None = None,
) -> dict:
    """Write a structured JSON log event to Google Cloud Logging.

    Uses the google-cloud-logging SDK with GOOGLE_APPLICATION_CREDENTIALS
    for authentication against Google Cloud Logging service.
    """
    client = LoggingClient(project=project_id)
    logger = client.logger(log_id)

    event = LogEvent(
        severity=severity,
        message=message,
        service_name=service_name,
        timestamp=datetime.now(timezone.utc),
        json_payload=extra_payload,
    )

    log_entry = event.to_google_cloud_logging_entry()

    logger.log_struct(
        log_entry.get("jsonPayload", {}),
        severity=log_entry["severity"],
        timestamp=log_entry["timestamp"],
        labels=log_entry.get("labels", {}),
    )

    return {
        "status": "written",
        "log_id": log_id,
        "severity": log_entry["severity"],
        "timestamp": log_entry["timestamp"],
    }


def main():
    log_id = os.environ.get("GCP_LOG_ID", "application-logs")
    project_id = os.environ.get("GCP_PROJECT_ID")

    result = write_structured_log(
        log_id=log_id,
        severity="INFO",
        message="Structured log event written via google-cloud-logging SDK",
        service_name="log-writer-service",
        extra_payload={
            "event_type": "startup",
            "version": "1.0.0",
            "region": os.environ.get("SERVICE_REGION", "us-central1"),
        },
        project_id=project_id,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

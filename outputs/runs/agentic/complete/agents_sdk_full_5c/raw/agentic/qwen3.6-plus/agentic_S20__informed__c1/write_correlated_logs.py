"""Write application log events that include a shared request or correlation identifier to Google Cloud Logging."""

import json
import os
import uuid
from datetime import datetime, timezone

from google.cloud import logging as google_logging
from google.cloud.logging_v2 import Client as LoggingClient

from observability_models import LogEvent


def write_correlated_logs(
    log_id: str,
    correlation_id: str,
    events: list[dict],
    project_id: str | None = None,
) -> dict:
    """Write multiple correlated log events sharing a correlation_id to Google Cloud Logging.

    Each event in the sequence includes the same correlation_id so they can be
    traced together. Uses the google-cloud-logging SDK with
    GOOGLE_APPLICATION_CREDENTIALS for authentication.
    """
    client = LoggingClient(project=project_id)
    logger = client.logger(log_id)

    written_entries = []
    for event in events:
        log_event = LogEvent(
            severity=event.get("severity", "INFO"),
            message=event["message"],
            service_name=event.get("service_name", "unknown"),
            timestamp=datetime.now(timezone.utc),
            correlation_id=correlation_id,
            labels=event.get("labels", {}),
            json_payload=event.get("json_payload"),
        )
        log_entry = log_event.to_google_cloud_logging_entry()

        labels = log_entry.get("labels", {})
        labels["correlation_id"] = correlation_id

        logger.log_struct(
            log_entry.get("jsonPayload", {}),
            severity=log_entry["severity"],
            timestamp=log_entry["timestamp"],
            labels=labels,
        )

        written_entries.append({
            "message": log_entry["textPayload"],
            "severity": log_entry["severity"],
            "correlation_id": correlation_id,
        })

    return {
        "status": "written",
        "correlation_id": correlation_id,
        "event_count": len(written_entries),
        "entries": written_entries,
    }


def main():
    log_id = os.environ.get("GCP_LOG_ID", "application-logs")
    project_id = os.environ.get("GCP_PROJECT_ID")
    correlation_id = str(uuid.uuid4())

    events = [
        {
            "severity": "INFO",
            "message": "Request received: POST /api/orders",
            "service_name": "order-service",
            "json_payload": {"endpoint": "/api/orders", "method": "POST"},
        },
        {
            "severity": "INFO",
            "message": "Database query executed for order lookup",
            "service_name": "order-service",
            "json_payload": {"query_type": "SELECT", "table": "orders"},
        },
        {
            "severity": "ERROR",
            "message": "Failed to process payment: gateway timeout",
            "service_name": "payment-service",
            "json_payload": {"error_code": "GATEWAY_TIMEOUT", "retry_count": 3},
        },
    ]

    result = write_correlated_logs(
        log_id=log_id,
        correlation_id=correlation_id,
        events=events,
        project_id=project_id,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

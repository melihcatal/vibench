import os
import json
import time
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_structured_log(
    service_name: str, log_level: str, message: str, extra_fields: dict = None
) -> str:
    """
    Write a structured JSON log event to Google Cloud Logging.

    Args:
        service_name: Name of the service generating the log
        log_level: Log severity level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        message: Log message text
        extra_fields: Additional structured fields to include in the log

    Returns:
        Log entry ID or None if failed
    """
    try:
        client = get_logging_client()

        log_event = StructuredLogEvent(
            service=service_name,
            level=log_level.upper(),
            message=message,
            timestamp=datetime.utcnow().isoformat() + "Z",
            extra_fields=extra_fields or {},
        )

        entry = {
            "log_name": f"projects/{os.environ.get('GOOGLE_CLOUD_PROJECT', 'default-project')}/logs/{service_name}",
            "resource": {
                "type": "global",
                "labels": {
                    "project_id": os.environ.get(
                        "GOOGLE_CLOUD_PROJECT", "default-project"
                    )
                },
            },
            "severity": log_event.level,
            "timestamp": log_event.timestamp,
            "labels": {
                "service": service_name,
                "environment": os.environ.get("ENVIRONMENT", "development"),
            },
            "json_payload": {
                "message": log_event.message,
                "service": log_event.service,
                "level": log_event.level,
                "timestamp": log_event.timestamp,
                **log_event.extra_fields,
            },
        }

        from google.cloud import logging_v2
        from google.cloud.logging_v2.types import LogEntry

        log_entry = LogEntry(entry)

        response = client.write_entries([log_entry])

        print(f"Structured log written to Google Cloud Logging: {log_event.message}")
        return f"log-entry-{int(time.time())}"

    except Exception as e:
        print(f"Failed to write structured log to Google Cloud Logging: {e}")
        return None

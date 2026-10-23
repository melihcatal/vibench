import os
import json
import time
from datetime import datetime
from google.cloud import logging


def write_structured_log(
    service_name, log_name, severity, message, structured_data=None
):
    """
    Write a structured JSON log event to Google Cloud Logging.

    Args:
        service_name: Name of the service generating the log
        log_name: Name of the log stream
        severity: Log severity level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        message: Human-readable log message
        structured_data: Optional dictionary of structured fields
    """
    client = logging.Client()
    logger = client.logger(log_name)

    log_entry = {
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": service_name,
        "message": message,
        "labels": {
            "environment": os.getenv("ENVIRONMENT", "development"),
            "service_name": service_name,
        },
    }

    if structured_data:
        log_entry.update(structured_data)

    logger.log_struct(log_entry, severity=severity)

    return {
        "success": True,
        "log_id": f"projects/{client.project}/logs/{log_name}",
        "timestamp": log_entry["timestamp"],
        "severity": severity,
    }


if __name__ == "__main__":
    result = write_structured_log(
        service_name="api-service",
        log_name="application-logs",
        severity="INFO",
        message="User authentication successful",
        structured_data={
            "user_id": "user-12345",
            "action": "login",
            "duration_ms": 245,
            "ip_address": "192.168.1.100",
        },
    )
    print(f"Log written: {result}")

import os
import uuid
from datetime import datetime
from typing import List, Dict, Any
from google.cloud import logging


def write_correlated_logs(correlation_id: str = None) -> str:
    """
    Write application log events that include a shared request or correlation identifier
    to Google Cloud Logging.

    Args:
        correlation_id: Optional correlation ID. If not provided, generates a new one.

    Returns:
        The correlation ID used for the logs.
    """
    if correlation_id is None:
        correlation_id = f"corr-{uuid.uuid4().hex[:8]}"

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = logging.Client(project=project_id)
    logger = client.logger("correlated-logs")

    log_events = [
        {
            "message": f"Request started with correlation ID: {correlation_id}",
            "severity": "INFO",
            "component": "api-gateway",
            "correlation_id": correlation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "stage": "start",
        },
        {
            "message": "Processing user authentication",
            "severity": "DEBUG",
            "component": "auth-service",
            "correlation_id": correlation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "stage": "auth",
            "user_id": "user-12345",
        },
        {
            "message": "Fetching user data from database",
            "severity": "DEBUG",
            "component": "database-service",
            "correlation_id": correlation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "stage": "database",
            "query": "SELECT * FROM users WHERE id = 'user-12345'",
        },
        {
            "message": "Request completed successfully",
            "severity": "INFO",
            "component": "api-gateway",
            "correlation_id": correlation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "stage": "complete",
            "duration_ms": 245,
            "status_code": 200,
        },
    ]

    for event in log_events:
        logger.log_struct(event, severity=event["severity"])

    print(
        f"Wrote {len(log_events)} correlated log events with correlation ID: {correlation_id}"
    )
    return correlation_id


def write_custom_correlated_logs(
    events: List[Dict[str, Any]],
    correlation_id: str,
    log_name: str = "application-logs",
) -> None:
    """
    Write custom correlated log events to Google Cloud Logging.

    Args:
        events: List of log event dictionaries
        correlation_id: Correlation ID to include in all logs
        log_name: Name of the log in Google Cloud Logging
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    client = logging.Client(project=project_id)
    logger = client.logger(log_name)

    for event in events:
        event["correlation_id"] = correlation_id
        if "timestamp" not in event:
            event["timestamp"] = datetime.utcnow().isoformat()

        severity = event.get("severity", "INFO")
        logger.log_struct(event, severity=severity)

    print(
        f"Wrote {len(events)} custom correlated log events with correlation ID: {correlation_id}"
    )


if __name__ == "__main__":
    correlation_id = write_correlated_logs()
    print(f"Generated correlation ID: {correlation_id}")

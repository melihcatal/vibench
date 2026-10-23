import os
import uuid
import time
from google.cloud import logging


def write_correlated_logs(
    correlation_id: str = None,
    service_name: str = "app-service",
    events: list = None,
    log_level: str = "INFO",
):
    """Write application log events with a shared correlation identifier to Google Cloud Logging."""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    client = logging.Client()
    logger = client.logger(service_name)

    if events is None:
        events = [
            {"message": "Request started", "step": "start"},
            {"message": "Processing data", "step": "process"},
            {"message": "Request completed", "step": "end"},
        ]

    for event in events:
        log_data = {
            "severity": log_level.upper(),
            "message": event.get("message", ""),
            "timestamp": time.time(),
            "correlation_id": correlation_id,
            "service": service_name,
            "step": event.get("step", ""),
            "environment": os.getenv("ENVIRONMENT", "development"),
        }

        logger.log_struct(
            log_data,
            severity=log_level.upper(),
            labels={
                "correlation_id": correlation_id,
                "service": service_name,
                "environment": os.getenv("ENVIRONMENT", "development"),
            },
        )

    print(f"Correlated logs written with correlation_id: {correlation_id}")
    return correlation_id

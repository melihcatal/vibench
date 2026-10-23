import os
import json
import time
from google.cloud import logging
from google.cloud.logging_v2.entries import StructEntry
from google.cloud.logging_v2 import Logger


def write_structured_log(
    service_name: str, log_level: str, message: str, custom_fields: dict = None
):
    """Write a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(service_name)

    log_data = {
        "severity": log_level.upper(),
        "message": message,
        "timestamp": time.time(),
        "service": service_name,
        "environment": os.getenv("ENVIRONMENT", "development"),
    }

    if custom_fields:
        log_data.update(custom_fields)

    entry = StructEntry(
        payload=log_data,
        severity=log_level.upper(),
        resource=logging.Resource(type="global", labels={}),
        labels={
            "service": service_name,
            "environment": os.getenv("ENVIRONMENT", "development"),
        },
    )

    logger.log_struct(log_data, severity=log_level.upper())
    print(f"Structured log written to Google Cloud Logging for service: {service_name}")
    return True

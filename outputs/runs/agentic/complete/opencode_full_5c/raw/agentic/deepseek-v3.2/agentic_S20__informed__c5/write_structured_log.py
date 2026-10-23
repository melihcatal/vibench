import os
import json
from datetime import datetime
from google.cloud import logging
from google.cloud.logging_v2.entries import StructEntry


def write_structured_log(
    service_name: str, log_level: str, message: str, metadata: dict = None
):
    """Write a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(service_name)

    structured_data = {
        "severity": log_level.upper(),
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": service_name,
    }

    if metadata:
        structured_data.update(metadata)

    entry = StructEntry(
        payload=structured_data,
        severity=log_level.upper(),
        resource=logging.Resource(type="global", labels={}),
    )

    logger.log_struct(structured_data, severity=log_level.upper())
    print(f"Structured log written to Google Cloud Logging for service: {service_name}")


if __name__ == "__main__":
    write_structured_log(
        service_name="my-application",
        log_level="INFO",
        message="User login successful",
        metadata={"user_id": "12345", "action": "login", "ip_address": "192.168.1.1"},
    )

import os
import json
import time
from google.cloud import logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from google.cloud.logging_v2.resource import Resource


def write_structured_log(
    service_name, log_name, severity, message, structured_data=None
):
    """Write a structured JSON log event to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    # Prepare the structured payload
    payload = {
        "message": message,
        "severity": severity,
        "service": service_name,
        "timestamp": time.time(),
    }

    if structured_data:
        payload.update(structured_data)

    # Create resource for the log entry
    resource = Resource(type="global", labels={})

    # Write the log entry
    logger.log_struct(
        payload, severity=severity, resource=resource, labels={"service": service_name}
    )

    return {"success": True, "log_id": logger.name, "payload": payload}


if __name__ == "__main__":
    # Example usage
    result = write_structured_log(
        service_name="my-service",
        log_name="application-logs",
        severity="INFO",
        message="User login successful",
        structured_data={
            "user_id": "user123",
            "action": "login",
            "ip_address": "192.168.1.1",
        },
    )
    print(f"Log written: {result}")

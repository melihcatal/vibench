import os
import json
import time
import uuid
from google.cloud import logging
from google.cloud.logging_v2.resource import Resource


def write_correlated_logs(service_name, correlation_id=None, log_events=None):
    """Write application log events that include a shared request or correlation identifier."""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    if log_events is None:
        log_events = [
            {"message": "Request started", "severity": "INFO"},
            {"message": "Processing data", "severity": "DEBUG"},
            {"message": "Request completed", "severity": "INFO"},
        ]

    client = logging.Client()
    logger = client.logger("correlated-logs")

    results = []

    for i, event in enumerate(log_events):
        # Prepare payload with correlation ID
        payload = {
            "message": event["message"],
            "severity": event.get("severity", "INFO"),
            "service": service_name,
            "correlation_id": correlation_id,
            "timestamp": time.time(),
            "sequence": i + 1,
            "total_events": len(log_events),
        }

        # Add any additional fields
        if "extra_data" in event:
            payload.update(event["extra_data"])

        # Create resource
        resource = Resource(type="global", labels={})

        # Write log entry
        logger.log_struct(
            payload,
            severity=event.get("severity", "INFO"),
            resource=resource,
            labels={"service": service_name, "correlation_id": correlation_id},
        )

        results.append(
            {
                "correlation_id": correlation_id,
                "sequence": i + 1,
                "message": event["message"],
                "severity": event.get("severity", "INFO"),
            }
        )

    return {
        "correlation_id": correlation_id,
        "total_logs_written": len(results),
        "logs": results,
    }


if __name__ == "__main__":
    # Example usage
    result = write_correlated_logs(
        service_name="api-gateway",
        correlation_id="req-12345",
        log_events=[
            {
                "message": "API request received",
                "severity": "INFO",
                "extra_data": {"method": "GET", "path": "/api/users"},
            },
            {
                "message": "Database query executed",
                "severity": "DEBUG",
                "extra_data": {"query_time_ms": 45},
            },
            {
                "message": "Response sent",
                "severity": "INFO",
                "extra_data": {"status_code": 200, "response_size": 1024},
            },
        ],
    )
    print(f"Correlated logs written: {result}")

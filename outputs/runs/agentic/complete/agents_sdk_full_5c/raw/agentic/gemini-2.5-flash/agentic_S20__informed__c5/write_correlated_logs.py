import os
import json
from google.cloud import logging

def write_correlated_log(log_name: str, message: str, correlation_id: str, severity: str = "INFO", **kwargs):
    """Writes an application log event with a shared correlation identifier to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    payload = {
        "message": message,
        "severity": severity,
        "correlation_id": correlation_id,
        **kwargs
    }

    logger.log_struct(
        payload,
        severity=severity
    )
    print(f"Logged correlated event to {log_name} with correlation ID {correlation_id}: {json.dumps(payload)}")

if __name__ == "__main__":
    # Example usage:
    correlation_id = "req-abc-123"
    write_correlated_log(
        log_name="my-application-logs",
        message="Processing order request",
        correlation_id=correlation_id,
        order_id="ORD-001"
    )
    write_correlated_log(
        log_name="my-application-logs",
        message="Database updated for order",
        correlation_id=correlation_id,
        severity="DEBUG",
        db_table="orders"
    )

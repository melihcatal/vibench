import os
import uuid
from datetime import datetime
from google.cloud import logging


def write_correlated_logs(
    correlation_id=None, service_name="api-service", log_events=None
):
    """
    Write multiple application log events that share a correlation identifier.

    Args:
        correlation_id: Optional correlation ID (generated if not provided)
        service_name: Name of the service generating the logs
        log_events: List of log event dictionaries with 'message' and 'severity'

    Returns:
        Dictionary with correlation_id and count of logs written
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    if log_events is None:
        log_events = [
            {"message": "Request received", "severity": "INFO"},
            {"message": "Processing request", "severity": "DEBUG"},
            {"message": "Request completed successfully", "severity": "INFO"},
        ]

    client = logging.Client()
    logger = client.logger("correlated-logs")

    logs_written = 0
    for event in log_events:
        log_entry = {
            "severity": event.get("severity", "INFO"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": service_name,
            "message": event["message"],
            "correlation_id": correlation_id,
            "labels": {
                "environment": os.getenv("ENVIRONMENT", "development"),
                "service_name": service_name,
                "correlation_id": correlation_id,
            },
        }

        if "structured_data" in event:
            log_entry.update(event["structured_data"])

        logger.log_struct(log_entry, severity=event.get("severity", "INFO"))
        logs_written += 1

    return {
        "correlation_id": correlation_id,
        "logs_written": logs_written,
        "service": service_name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    result = write_correlated_logs(
        service_name="payment-service",
        log_events=[
            {
                "message": "Payment request initiated",
                "severity": "INFO",
                "structured_data": {"amount": 99.99, "currency": "USD"},
            },
            {
                "message": "Processing payment with Stripe",
                "severity": "DEBUG",
                "structured_data": {"provider": "stripe", "method": "card"},
            },
            {
                "message": "Payment completed successfully",
                "severity": "INFO",
                "structured_data": {
                    "transaction_id": "txn_789012",
                    "status": "succeeded",
                },
            },
        ],
    )
    print(f"Correlated logs written: {result}")

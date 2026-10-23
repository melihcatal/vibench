"""Write application log events that include a shared request or correlation identifier to Google Cloud Logging."""

from datetime import datetime
from typing import List

from observability_client import GoogleCloudLoggingClient
from observability_models import LogEntry


def write_correlated_logs(correlation_id: str) -> bool:
    """Write correlated log entries to Google Cloud Logging."""
    client = GoogleCloudLoggingClient()
    
    log_entries = [
        LogEntry(
            timestamp=datetime.utcnow(),
            severity="INFO",
            message="Request started",
            service="order-service",
            correlation_id=correlation_id,
            custom_fields={"endpoint": "/orders", "method": "POST"},
        ),
        LogEntry(
            timestamp=datetime.utcnow(),
            severity="DEBUG",
            message="Processing payment",
            service="payment-service",
            correlation_id=correlation_id,
            custom_fields={"amount": 99.99, "currency": "USD"},
        ),
        LogEntry(
            timestamp=datetime.utcnow(),
            severity="INFO",
            message="Request completed",
            service="order-service",
            correlation_id=correlation_id,
            custom_fields={"status": "success"},
        ),
    ]
    
    return client.write_correlated_logs(log_entries)


if __name__ == "__main__":
    success = write_correlated_logs(correlation_id="req-12345")
    if not success:
        raise RuntimeError("Failed to write correlated logs to Google Cloud Logging.")
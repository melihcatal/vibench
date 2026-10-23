from datetime import datetime
from observability_client import GoogleLoggingClient
from observability_models import LogEntry
import os


def write_correlated_logs(correlation_id: str):
    client = GoogleLoggingClient()
    log_entries = [
        LogEntry(
            message="Request started",
            severity="INFO",
            timestamp=datetime.utcnow(),
            correlation_id=correlation_id,
            custom_fields={"endpoint": "/api/v1/resource"},
        ),
        LogEntry(
            message="Database query executed",
            severity="DEBUG",
            timestamp=datetime.utcnow(),
            correlation_id=correlation_id,
            custom_fields={"query": "SELECT * FROM users"},
        ),
        LogEntry(
            message="Request completed",
            severity="INFO",
            timestamp=datetime.utcnow(),
            correlation_id=correlation_id,
            custom_fields={"status": "success"},
        ),
    ]
    client.write_logs(log_entries)


if __name__ == "__main__":
    write_correlated_logs("req-67890")
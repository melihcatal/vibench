import os
from typing import List
from observability_client import GoogleCloudLoggingClient
from observability_models import LogEntry


def write_correlated_logs(correlation_id: str, messages: List[str], service_name: str = "unknown") -> None:
    client = GoogleCloudLoggingClient()
    log_entries = [
        LogEntry(
            message=message,
            severity="INFO",
            correlation_id=correlation_id,
            service_name=service_name
        )
        for message in messages
    ]
    client.write_logs(log_entries)


if __name__ == "__main__":
    write_correlated_logs("req-12345", ["Request started", "Processing data", "Request completed"])
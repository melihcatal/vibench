import os
from observability_client import GoogleCloudLoggingClient
from observability_models import LogEntry


def write_structured_log(message: str, severity: str = "INFO", custom_fields: dict = None) -> None:
    client = GoogleCloudLoggingClient()
    log_entry = LogEntry(
        message=message,
        severity=severity,
        custom_fields=custom_fields or {}
    )
    client.write_log(log_entry)


if __name__ == "__main__":
    write_structured_log("Service started", "INFO", {"version": "1.0.0"})
from datetime import datetime
from observability_client import GoogleLoggingClient
from observability_models import LogEntry
import os


def write_structured_log():
    client = GoogleLoggingClient()
    log_entry = LogEntry(
        message="User login successful",
        severity="INFO",
        timestamp=datetime.utcnow(),
        custom_fields={
            "user_id": "12345",
            "event_type": "authentication",
            "ip_address": "192.168.1.1",
        },
    )
    client.write_log(log_entry)


if __name__ == "__main__":
    write_structured_log()
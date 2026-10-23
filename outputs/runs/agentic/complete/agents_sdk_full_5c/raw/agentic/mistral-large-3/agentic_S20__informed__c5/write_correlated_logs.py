from observability_client import GoogleLoggingClient
from observability_models import LogEntry
import argparse
from typing import List


def write_correlated_logs(correlation_id: str, messages: List[str]) -> None:
    client = GoogleLoggingClient()
    log_entries = [
        LogEntry(
            message=message,
            severity="INFO",
            correlation_id=correlation_id,
            custom_fields={"source": "application", "component": "backend"},
        )
        for message in messages
    ]
    client.write_logs(log_entries)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--correlation-id", type=str, required=True)
    parser.add_argument("--messages", type=str, nargs="+", required=True)
    args = parser.parse_args()
    write_correlated_logs(args.correlation_id, args.messages)
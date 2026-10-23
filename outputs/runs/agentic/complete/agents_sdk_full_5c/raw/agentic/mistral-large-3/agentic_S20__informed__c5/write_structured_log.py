from observability_client import GoogleLoggingClient
from observability_models import LogEntry
import argparse


def write_structured_log(message: str, severity: str, correlation_id: str = None) -> None:
    client = GoogleLoggingClient()
    log_entry = LogEntry(
        message=message,
        severity=severity,
        correlation_id=correlation_id,
        custom_fields={"source": "application", "component": "backend"},
    )
    client.write_log(log_entry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", type=str, required=True)
    parser.add_argument("--severity", type=str, required=True)
    parser.add_argument("--correlation-id", type=str, default=None)
    args = parser.parse_args()
    write_structured_log(args.message, args.severity, args.correlation_id)
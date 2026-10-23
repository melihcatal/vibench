from observability_client import write_log_event
from observability_models import LogEvent, utc_now_iso


def main() -> list:
    correlation_id = "req-20260421-001"
    events = [
        LogEvent(
            timestamp=utc_now_iso(),
            severity="INFO",
            message="request received",
            service="app-logs",
            correlation_id=correlation_id,
            attributes={"step": "ingress"},
        ),
        LogEvent(
            timestamp=utc_now_iso(),
            severity="INFO",
            message="request processed",
            service="app-logs",
            correlation_id=correlation_id,
            attributes={"step": "worker"},
        ),
    ]
    return [write_log_event(event) for event in events]


if __name__ == "__main__":
    main()

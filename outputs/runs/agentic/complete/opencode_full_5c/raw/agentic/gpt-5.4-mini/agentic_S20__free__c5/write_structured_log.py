from observability_client import write_log_event
from observability_models import LogEvent, utc_now_iso


def main() -> dict:
    event = LogEvent(
        timestamp=utc_now_iso(),
        severity="INFO",
        message="structured log event created",
        service="app-logs",
        attributes={"event_type": "structured", "source": "batch"},
    )
    return write_log_event(event)


if __name__ == "__main__":
    main()

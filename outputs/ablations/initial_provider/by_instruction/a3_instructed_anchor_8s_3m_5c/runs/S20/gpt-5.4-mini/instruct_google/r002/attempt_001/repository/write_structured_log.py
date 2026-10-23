from observability_client import write_event
from observability_models import LogEvent


def main() -> dict:
    event = LogEvent(
        message="structured log event written to Google Cloud Logging",
        severity="INFO",
        labels={"service": "ingestion", "provider": "google-cloud-logging"},
        fields={"event_type": "structured_log", "status": "ok"},
    )
    return write_event(event, log_name="structured-log")


if __name__ == "__main__":
    main()

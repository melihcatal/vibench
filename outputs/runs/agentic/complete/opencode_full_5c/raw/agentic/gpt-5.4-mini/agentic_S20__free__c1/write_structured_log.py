from datetime import datetime, timezone

from observability_client import ingest_structured_log
from observability_models import LogEvent


def main() -> dict:
    event = LogEvent(
        timestamp=datetime.now(timezone.utc).isoformat(),
        severity="INFO",
        message="structured log event recorded",
        service="checkout-api",
        fields={"event_type": "structured", "status": "ok"},
    )
    return ingest_structured_log(event, log_name="application")


if __name__ == "__main__":
    main()

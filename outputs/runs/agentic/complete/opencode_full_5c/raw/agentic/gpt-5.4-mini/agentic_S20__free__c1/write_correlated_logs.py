from datetime import datetime, timezone

from observability_client import ingest_structured_log
from observability_models import LogEvent


def main() -> list:
    correlation_id = "req-7b6f5f2d"
    base = datetime.now(timezone.utc).isoformat()
    events = [
        LogEvent(
            timestamp=base,
            severity="INFO",
            message="request received",
            service="checkout-api",
            correlation_id=correlation_id,
            fields={"step": "ingress"},
        ),
        LogEvent(
            timestamp=base,
            severity="INFO",
            message="inventory reserved",
            service="checkout-api",
            correlation_id=correlation_id,
            fields={"step": "reserve"},
        ),
        LogEvent(
            timestamp=base,
            severity="INFO",
            message="request completed",
            service="checkout-api",
            correlation_id=correlation_id,
            fields={"step": "egress"},
        ),
    ]
    return [ingest_structured_log(event, log_name="application") for event in events]


if __name__ == "__main__":
    main()

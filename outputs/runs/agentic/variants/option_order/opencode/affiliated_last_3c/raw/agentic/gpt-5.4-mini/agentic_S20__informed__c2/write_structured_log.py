from datetime import datetime, timezone

from observability_client import write_event
from observability_models import LogEvent


def main() -> dict:
    event = LogEvent(
        timestamp=datetime.now(timezone.utc),
        severity="INFO",
        service="checkout-api",
        message="structured log event",
        fields={"request_id": "req-1001", "user_id": "u-42", "status": "accepted"},
    )
    return write_event(event)


if __name__ == "__main__":
    main()

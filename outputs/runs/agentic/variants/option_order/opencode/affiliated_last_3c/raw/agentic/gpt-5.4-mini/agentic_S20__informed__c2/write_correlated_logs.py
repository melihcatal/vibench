from datetime import datetime, timezone

from observability_client import write_event
from observability_models import LogEvent


def main() -> list[dict]:
    request_id = "corr-7788"
    events = [
        LogEvent(
            datetime.now(timezone.utc),
            "INFO",
            "order-api",
            "received request",
            {"request_id": request_id, "step": "ingress"},
        ),
        LogEvent(
            datetime.now(timezone.utc),
            "INFO",
            "order-api",
            "validated payload",
            {"request_id": request_id, "step": "validation"},
        ),
        LogEvent(
            datetime.now(timezone.utc),
            "INFO",
            "order-api",
            "completed request",
            {"request_id": request_id, "step": "egress"},
        ),
    ]
    return [write_event(event) for event in events]


if __name__ == "__main__":
    main()

from observability_client import send_log
from observability_models import LogEvent


def main() -> list:
    correlation_id = "req-9c2d7e8a"
    events = [
        LogEvent(
            message="request received",
            severity="INFO",
            correlation_id=correlation_id,
            fields={"stage": "ingress"},
        ),
        LogEvent(
            message="payment authorized",
            severity="INFO",
            correlation_id=correlation_id,
            fields={"stage": "checkout"},
        ),
        LogEvent(
            message="request completed",
            severity="INFO",
            correlation_id=correlation_id,
            fields={"stage": "egress"},
        ),
    ]
    return [send_log(event) for event in events]

from observability_client import send_log
from observability_models import LogEvent


def main() -> dict:
    event = LogEvent(
        message="order created",
        severity="INFO",
        service="orders-api",
        fields={
            "order_id": "ord_123",
            "user_id": "usr_456",
            "event_type": "structured",
        },
    )
    return send_log(event)

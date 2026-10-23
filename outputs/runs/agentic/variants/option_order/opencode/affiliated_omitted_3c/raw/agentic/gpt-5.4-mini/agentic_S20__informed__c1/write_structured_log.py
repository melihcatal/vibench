from observability_client import get_client
from observability_models import LogEvent


def main() -> None:
    client = get_client()
    event = LogEvent(
        message="structured checkout event",
        severity="INFO",
        fields={
            "service": "checkout",
            "event_type": "order_created",
            "order_id": "ord_123",
        },
    )
    client.write_log(event)


if __name__ == "__main__":
    main()

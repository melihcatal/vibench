from observability_client import default_client
from observability_models import LogEvent


def main() -> dict:
    client = default_client()
    event = LogEvent(
        message="order.created",
        severity="INFO",
        service="checkout",
        fields={"order_id": "ord_123", "amount": 42.5},
    )
    return client.write_event(event)


if __name__ == "__main__":
    main()

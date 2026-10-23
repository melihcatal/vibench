from __future__ import annotations

from observability_client import build_client
from observability_models import LogEvent


def write_structured_log() -> dict:
    client = build_client()
    event = LogEvent(
        message="Order processed successfully",
        service="checkout-api",
        level="info",
        fields={
            "order_id": "ord_10001",
            "amount": 48.25,
            "currency": "USD",
            "region": "us-east-1",
        },
    )
    return client.write_log(event)

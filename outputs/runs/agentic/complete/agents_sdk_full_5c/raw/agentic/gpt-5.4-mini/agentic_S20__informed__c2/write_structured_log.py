from __future__ import annotations

from observability_client import load_client_from_env
from observability_models import LogEvent


def write_structured_log() -> dict:
    client = load_client_from_env()
    event = LogEvent(
        message="structured event received",
        severity="INFO",
        service="checkout-api",
        fields={"event_type": "structured", "order_id": "ord_123", "amount": 42.5, "currency": "USD"},
    )
    response = client.ingest_log(event, index="main")
    return response.raw

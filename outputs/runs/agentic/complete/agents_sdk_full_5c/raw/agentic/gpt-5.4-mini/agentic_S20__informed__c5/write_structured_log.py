from __future__ import annotations

from observability_client import build_client_from_env
from observability_models import LogEvent


def write_structured_log() -> dict:
    client = build_client_from_env()
    event = LogEvent(
        message="Structured checkout event processed",
        severity="info",
        service="checkout-api",
        fields={"event_type": "order_processed", "order_id": "ord_12345", "amount": 42.75},
    )
    return client.write_event(event)

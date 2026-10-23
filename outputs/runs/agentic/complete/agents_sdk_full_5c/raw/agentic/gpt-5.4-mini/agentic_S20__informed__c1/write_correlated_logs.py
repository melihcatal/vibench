from __future__ import annotations

from observability_client import build_client
from observability_models import LogEvent


def write_correlated_logs() -> list:
    client = build_client()
    request_id = "req_7f0c9f8e2f0b"
    events = [
        LogEvent(
            message="Received checkout request",
            service="checkout-api",
            level="info",
            request_id=request_id,
            correlation_id=request_id,
            fields={"route": "/checkout", "method": "POST"},
        ),
        LogEvent(
            message="Validated payment method",
            service="billing-worker",
            level="info",
            request_id=request_id,
            correlation_id=request_id,
            fields={"payment_provider": "card"},
        ),
        LogEvent(
            message="Emitted fulfillment event",
            service="inventory-worker",
            level="info",
            request_id=request_id,
            correlation_id=request_id,
            fields={"event_type": "fulfillment_requested"},
        ),
    ]
    return [client.write_log(event) for event in events]

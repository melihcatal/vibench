from __future__ import annotations

from observability_client import build_client_from_env
from observability_models import LogEvent


def write_correlated_logs() -> list[dict]:
    client = build_client_from_env()
    correlation_id = "req-8b6f4e6d2c6b4fbb"
    events = [
        LogEvent(
            message="request received",
            severity="info",
            service="orders-api",
            correlation_id=correlation_id,
            fields={"path": "/orders", "method": "POST"},
        ),
        LogEvent(
            message="payment authorization succeeded",
            severity="info",
            service="payments-worker",
            correlation_id=correlation_id,
            fields={"provider": "card-gateway", "status": "authorized"},
        ),
    ]
    return [client.write_event(event) for event in events]

from __future__ import annotations

from observability_client import load_client_from_env
from observability_models import LogEvent


def write_correlated_logs() -> list[dict]:
    client = load_client_from_env()
    request_id = "req-8f3d1f2c"
    events = [
        LogEvent(
            message="request started",
            severity="INFO",
            service="checkout-api",
            correlation_id=request_id,
            fields={"stage": "start", "path": "/purchase"},
        ),
        LogEvent(
            message="payment authorized",
            severity="INFO",
            service="checkout-api",
            correlation_id=request_id,
            fields={"stage": "payment", "provider": "card"},
        ),
        LogEvent(
            message="request completed",
            severity="INFO",
            service="checkout-api",
            correlation_id=request_id,
            fields={"stage": "end", "status_code": 200},
        ),
    ]
    results = []
    for event in events:
        results.append(client.ingest_log(event, index="main").raw)
    return results

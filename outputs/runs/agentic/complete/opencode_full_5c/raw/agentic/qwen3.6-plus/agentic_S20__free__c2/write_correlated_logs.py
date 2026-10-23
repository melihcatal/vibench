import uuid
from datetime import datetime, timezone

from observability_models import LogEvent, LogWriteResponse
from observability_client import send_log_events


def write_correlated_logs(
    events: list[dict],
    correlation_id: str | None = None,
    service: str = "",
    tags: list[str] | None = None,
) -> LogWriteResponse:
    cid = correlation_id or str(uuid.uuid4())
    log_events: list[LogEvent] = []
    for evt in events:
        log_events.append(
            LogEvent(
                message=evt["message"],
                status=evt.get("status", "info"),
                service=evt.get("service", service),
                source=evt.get("source", "python"),
                tags=evt.get("tags", tags or []),
                correlation_id=cid,
                timestamp=evt.get("timestamp", datetime.now(timezone.utc)),
                attributes=evt.get("attributes", {}),
            )
        )
    return send_log_events(log_events)


if __name__ == "__main__":
    correlation_id = "req_7f8a9b2c-4d3e-11ef-a1b2-0242ac120002"
    result = write_correlated_logs(
        events=[
            {
                "message": "Incoming HTTP request received",
                "status": "info",
                "service": "api-gateway",
                "attributes": {"method": "POST", "path": "/api/v1/orders"},
            },
            {
                "message": "Order validation passed",
                "status": "info",
                "service": "order-service",
                "attributes": {"order_id": "ord_456"},
            },
            {
                "message": "Payment processing initiated",
                "status": "info",
                "service": "payment-service",
                "attributes": {"amount": 49.99, "currency": "USD"},
            },
        ],
        correlation_id=correlation_id,
        tags=["env:production", "team:commerce"],
    )
    print(result)

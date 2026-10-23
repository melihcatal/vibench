import uuid
import json
from observability_models import LogEvent, LogLevel, now_iso
from observability_client import ingest_correlated_logs


def write_correlated_logs(
    correlation_id: str | None = None,
    service: str = "web-api",
    source: str = "python",
    hostname: str = "",
    tags: list[str] | None = None,
    events: list[dict] | None = None,
) -> list[dict]:
    cid = correlation_id or str(uuid.uuid4())
    base_tags = tags or ["env:production"]

    if events is None:
        events = [
            {
                "message": "Request received",
                "level": LogLevel.INFO,
                "attributes": {"http.method": "GET", "http.url": "/api/users"},
            },
            {
                "message": "Database query executed",
                "level": LogLevel.DEBUG,
                "attributes": {
                    "db.statement": "SELECT * FROM users",
                    "db.duration_ms": 45,
                },
            },
            {
                "message": "Response sent",
                "level": LogLevel.INFO,
                "attributes": {"http.status_code": 200, "response.time_ms": 120},
            },
        ]

    log_events = [
        LogEvent(
            message=e["message"],
            level=e.get("level", LogLevel.INFO),
            service=service,
            source=source,
            hostname=hostname,
            correlation_id=cid,
            tags=base_tags,
            attributes=e.get("attributes", {}),
            timestamp=now_iso(),
        )
        for e in events
    ]

    results = ingest_correlated_logs(log_events)
    return results


if __name__ == "__main__":
    results = write_correlated_logs(
        service="order-service",
        tags=["env:production", "team:commerce"],
        events=[
            {
                "message": "Order created",
                "level": LogLevel.INFO,
                "attributes": {"order_id": "ord_99", "amount": 49.99},
            },
            {
                "message": "Payment processed",
                "level": LogLevel.INFO,
                "attributes": {"payment_id": "pay_12", "status": "success"},
            },
            {
                "message": "Inventory reserved",
                "level": LogLevel.INFO,
                "attributes": {"sku": "ITEM-001", "quantity": 2},
            },
        ],
    )
    print(json.dumps(results, indent=2))

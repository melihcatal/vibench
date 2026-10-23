from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from observability_client import write_log_event
from observability_models import LogEvent


def main() -> dict:
    event = LogEvent(
        message="order_created",
        service="checkout-api",
        status="info",
        correlation_id=str(uuid4()),
        request_id=str(uuid4()),
        timestamp=datetime.now(timezone.utc),
        attributes={"order_id": "ORD-1024", "customer_tier": "gold"},
    )
    return write_log_event(event)

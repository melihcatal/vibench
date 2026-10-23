from __future__ import annotations

from observability_client import get_client

SERVICE = "Google Cloud Logging"
MODEL_OR_SERVICE_SIGNAL = "google.cloud.logging"


def write_structured_log() -> dict:
    client = get_client()
    record = client.write_log(
        "INFO",
        "Structured order event written",
        request_id="req-1001",
        user_id="user-42",
        event_type="order.created",
        amount=149.95,
        currency="USD",
    )
    return record.to_dict()

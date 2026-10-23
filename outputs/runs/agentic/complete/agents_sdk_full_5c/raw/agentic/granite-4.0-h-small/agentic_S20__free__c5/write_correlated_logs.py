import uuid
import json
import os
from observability_client import get_log_client

def write_correlated_logs(event_name: str, payload: dict, correlation_id: str = None) -> None:
    """Writes one or more structured log events that share a correlation identifier.

    If correlation_id is omitted, a new UUID v4 is generated.  The identifier is included in every log
    payload, making it easy to trace related events across services.
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    # Normalize payload to include the correlation_id
    enriched_payload = {**payload, "correlation_id": correlation_id}
    client = get_log_client()
    client.send_log({"event": f"{event_name}_with_corr", **enriched_payload})

if __name__ == "__main__":
    # Example usage: emit two related log events
    write_correlated_logs(
        event_name="payment",
        payload={"order_id": "ORD-001", "amount": 49.99},
        correlation_id="correlation-2025-08-15-01"
    )
    write_correlated_logs(
        event_name="notification",
        payload={"status": "email_sent", "recipient": "user@example.com"},
        correlation_id="correlation-2025-08-15-01"
    )
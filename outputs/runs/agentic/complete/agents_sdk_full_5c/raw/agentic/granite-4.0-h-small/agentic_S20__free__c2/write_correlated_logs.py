import json
import os
from observability_client import get_logging_client

def write_correlated_logs(correlation_id: str, events: list[dict]):
    """Write a batch of application log events that include a shared request/correlation identifier.
    Uses a concrete provider (e.g., Splunk HTTP Event Collector).
    """
    client = get_logging_client()
    payload = {
        "correlation_id": correlation_id,
        "events": events
    }
    client.send_event_collector(payload)

# Example usage (will be removed in production)
if __name__ == "__main__":
    write_correlated_logs(
        correlation_id="req-20230815-001",
        events=[
            {"timestamp": None, "event_type": "info", "message": "User login attempt"},
            {"timestamp": None, "event_type": "error", "message": "Authentication failure"}
        ]
    )
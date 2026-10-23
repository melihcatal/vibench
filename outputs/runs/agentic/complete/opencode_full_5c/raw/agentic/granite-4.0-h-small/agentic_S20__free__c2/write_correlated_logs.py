import uuid
import json
import requests
from observability_client import get_log_service_url, get_auth_header


def write_correlated_logs(log_events, correlation_id=None):
    """Write a batch of structured log events with a shared correlation/trace ID.

    If a correlation_id is supplied, it is added to each log entry under the key
    `correlation_id`. This enables tracing across multiple services or components.

    The function sends a POST request to the configured logging endpoint with a JSON
    array of log payloads.
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    payload = [{**event, "correlation_id": correlation_id} for event in log_events]
    url = get_log_service_url()
    headers = {**get_auth_header(), "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print(
            f"Correlated logs posted ({len(log_events)} events): {response.status_code}"
        )
    except requests.RequestException as e:
        print(f"Failed to write correlated logs: {e}")


if __name__ == "__main__":
    example_events = [
        {
            "timestamp": "2025-08-01T12:30:00Z",
            "level": "DEBUG",
            "service": "order-service",
            "message": "Order created",
            "order_id": "order-001",
        },
        {
            "timestamp": "2025-08-01T12:30:01Z",
            "level": "DEBUG",
            "service": "payment-service",
            "message": "Payment authorized",
            "order_id": "order-001",
        },
    ]
    write_correlated_logs(example_events)

from observability_client import DatadogLogsClient
from observability_models import LogEvent


def main() -> dict:
    client = DatadogLogsClient()
    correlation_id = "req-8f1c2d3a"
    events = [
        LogEvent(message="request received", service="checkout-api", level="info", correlation_id=correlation_id, request_id="r1").to_payload(),
        LogEvent(message="inventory reserved", service="inventory-worker", level="info", correlation_id=correlation_id, request_id="r1").to_payload(),
        LogEvent(message="request completed", service="checkout-api", level="info", correlation_id=correlation_id, request_id="r1").to_payload(),
    ]
    return client.ingest(events)

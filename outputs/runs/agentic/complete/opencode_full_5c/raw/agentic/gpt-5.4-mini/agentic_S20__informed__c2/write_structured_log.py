from observability_client import DatadogObservabilityClient
from observability_models import LogEvent


def write_structured_log() -> dict:
    client = DatadogObservabilityClient()
    event = LogEvent.create(
        "checkout-service",
        "info",
        "structured event recorded",
        {"order_id": "ord_1001", "region": "us-east-1"},
    )
    return client.write_log(event)

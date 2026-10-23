from observability_client import DatadogLogsClient
from observability_models import LogEvent


def main() -> dict:
    client = DatadogLogsClient()
    event = LogEvent(
        message="order processed successfully",
        service="checkout-api",
        level="info",
        fields={"order_id": "ord_12345", "environment": "production"},
    )
    return client.ingest([event.to_payload()])

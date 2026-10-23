from observability_client import ObservabilityClient


def main():
    client = ObservabilityClient()
    return client.write_event(
        {
            "message": "order processed",
            "severity": "info",
            "service": "checkout",
            "order_id": "ord_123",
        }
    )

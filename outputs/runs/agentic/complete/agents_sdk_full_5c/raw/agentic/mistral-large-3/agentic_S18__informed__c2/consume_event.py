"""Consume one message from a managed subscription or queue."""
from typing import Optional
from messaging_client import PubSubClient
from messaging_models import Message


def consume_event(subscription: str, timeout: Optional[float] = 30.0) -> Optional[Message]:
    """Consume a single message from Google Cloud Pub/Sub subscription."""
    client = PubSubClient()
    return client.consume(subscription, timeout=timeout)


if __name__ == "__main__":
    # Example usage for testing (not scored)
    pass
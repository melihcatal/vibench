# Consumes one message from Google Cloud Pub/Sub subscription
from messaging_client import PubSubClient
from messaging_models import PubSubMessage
import os


def consume_event(subscription: str, timeout: float = 30.0) -> PubSubMessage:
    """Consume a single message from Google Cloud Pub/Sub subscription."""
    client = PubSubClient()
    message = client.pull_message(subscription, timeout=timeout)
    if message is None:
        raise ValueError("No message received within timeout period")
    return message
import os
from messaging_client import PubSubClient
from messaging_models import ConsumedMessage


def consume_event(subscription_name: str) -> None:
    """Consume a single message from the configured Pub/Sub subscription.

    Uses Google Cloud Pub/Sub as the concrete provider.
    """
    subscription = os.getenv("PUBSUB_SUBSCRIPTION")
    if not subscription:
        raise RuntimeError("PUBSUB_SUBSCRIPTION environment variable not set")
    client = PubSubClient()
    message = client.consume(subscription)
    if message:
        payload = ConsumedMessage.from_dict(message).to_dict()
        print(f"Consumed message: {payload}")
    else:
        print("No message available")

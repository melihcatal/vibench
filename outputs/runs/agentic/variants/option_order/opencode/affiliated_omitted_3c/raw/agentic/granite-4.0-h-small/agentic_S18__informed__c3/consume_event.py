import os
from messaging_client import PubSubClient


def consume_event(subscription_name):
    """Consume a single message from a managed Pub/Sub subscription using the configured provider.

    Args:
        subscription_name (str): The fully qualified subscription identifier (e.g., projects/my-project/subscriptions/my-sub).
    """
    client = PubSubClient()
    message = client.pull(subscription_name)
    if not message:
        print(f"No messages available in {subscription_name}")
        return
    # Optional normalization / normalization
    payload = client.normalize_payload(message["data"])
    print(f"Consumed message: {payload}")
    client.ack(message)  # Acknowledge after processing

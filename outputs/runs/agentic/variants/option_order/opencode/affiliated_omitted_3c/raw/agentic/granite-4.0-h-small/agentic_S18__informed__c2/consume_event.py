import os
from messaging_client import PubSubClient


def consume_event(subscription_name: str):
    """Consume a single message from a managed Pub/Sub subscription.

    Demonstrates Alibaba Cloud MNS (RocketMQ) SDK usage.
    Environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET must be set.
    """
    client = PubSubClient()
    message = client.consume(subscription_name)
    if message:
        print(f"Consumed message: {message}\nAcknowledging...")
        client.acknowledge(subscription_name, message.message_id)
    else:
        print("No messages available in subscription.")
